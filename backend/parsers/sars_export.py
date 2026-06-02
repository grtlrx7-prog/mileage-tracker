import json
import os
import pandas as pd

from backend.db.database import SessionLocal
from backend.db.models import Trip

from backend.ai.classifier import classify_trip

from backend.utils.location_clusters import LocationClusterer
from backend.utils.address_engine import get_address
from backend.utils.location_learning import detect_home, detect_work
from backend.utils.review_queue import build_review_queue
from backend.utils.audit_pack import build_audit_summary
from backend.utils.pdf_report import generate_pdf_report

from backend.utils.memory_engine import (
    update_memory,
    get_best_home,
    get_best_work
)

from backend.utils.ml_engine import MileageML
from backend.utils.self_heal_engine import SelfHealingEngine


# =================================================
# CONFIG
# =================================================

INPUT_FILE = "backend/data/timeline.json"

OUTPUT_FILE = "backend/exports/mileage_logbook.xlsx"

PDF_OUTPUT = "backend/exports/sars_audit_report.pdf"

RATE_PER_KM = 4.64

TAX_YEAR = "2025/2026"


# =================================================
# MAIN FUNCTION
# =================================================

def parse_timeline(user_id=1):

    print("====================================")
    print("🔥 SARS EXPORT STARTED")
    print("====================================")

    db = SessionLocal()

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("semanticSegments", [])

    print(f"📦 Segments loaded: {len(segments)}")

    rows = []

    clusterer = LocationClusterer(radius_km=0.8)

    ml_engine = MileageML()

    healer = SelfHealingEngine()

    created = 0

    # =================================================
    # PROCESS DATA
    # =================================================

    for i, s in enumerate(segments):

        if i % 100 == 0:

            print(
                f"Heartbeat → Processing segment {i}/{len(segments)}"
            )

        activity = s.get("activity", {})

        start = s.get("startTime")
        end = s.get("endTime")

        if not start or not end:
            continue

        try:

            start_dt = pd.to_datetime(start, utc=True)

            end_dt = pd.to_datetime(end, utc=True)

        except:
            continue

        distance = activity.get("distanceMeters", 0) or 0

        km = round(distance / 1000, 2)

        if km <= 0.3:
            continue

        # =================================================
        # COORDINATES
        # =================================================

        start_latlng = healer.fix_latlng({
            "latitudeE7": activity.get("startLatitudeE7"),
            "longitudeE7": activity.get("startLongitudeE7")
        })

        end_latlng = healer.fix_latlng({
            "latitudeE7": activity.get("endLatitudeE7"),
            "longitudeE7": activity.get("endLongitudeE7")
        })

        latitude = None
        longitude = None

        try:

            latitude = (
                start_latlng["latitudeE7"] / 10000000
            )

            longitude = (
                start_latlng["longitudeE7"] / 10000000
            )

        except:
            pass

        # =================================================
        # ADDRESS
        # =================================================

        from_addr = healer.fix_address(
            get_address(start_latlng)
        )

        to_addr = healer.fix_address(
            get_address(end_latlng)
        )

        # =================================================
        # CLUSTER LEARNING
        # =================================================

        clusterer.learn_location(from_addr)

        clusterer.learn_location(to_addr)

        # =================================================
        # AI CLASSIFICATION
        # =================================================

        ai_result = classify_trip(
            from_addr,
            to_addr
        )

        trip_type = ai_result["trip_type"]

        purpose = ai_result["reason"]

        confidence = ai_result["confidence"]

        risk_level = ai_result["risk_level"]

        duration = round(
            (end_dt - start_dt).total_seconds() / 60,
            1
        )

        # =================================================
        # DATAFRAME ROW
        # =================================================

        rows.append({

            "Date": start_dt.date(),

            "Start Time": start_dt,

            "End Time": end_dt,

            "Duration (min)": duration,

            "From": from_addr,

            "To": to_addr,

            "KM": km,

            "Trip Type": trip_type,

            "Purpose": purpose,

            "Confidence": confidence,

            "Risk Level": risk_level,

            "From Coordinates": str(start_latlng),

            "To Coordinates": str(end_latlng),
        })

        # =================================================
        # DATABASE SAVE
        # =================================================

        trip = Trip(

            user_id=user_id,

            date=str(start_dt.date()),

            start_time=start_dt.to_pydatetime(),

            end_time=end_dt.to_pydatetime(),

            from_location=from_addr,

            to_location=to_addr,

            latitude=str(latitude),

            longitude=str(longitude),

            km=str(km),

            trip_type=trip_type,

            purpose=purpose,

            confidence=str(confidence),

            risk_level=risk_level
        )

        db.add(trip)

        created += 1

    # =================================================
    # SAVE DATABASE
    # =================================================

    db.commit()

    db.close()

    # =================================================
    # DATAFRAME
    # =================================================

    df = pd.DataFrame(rows)

    if df.empty:

        print("⚠️ No trips found.")

        return

    df = df.sort_values(
        "Start Time"
    ).reset_index(drop=True)

    print(f"✅ Trips created: {len(df)}")

    # =================================================
    # ML ENGINE
    # =================================================

    ml_engine.train(df)

    # =================================================
    # HOME / WORK
    # =================================================

    home = detect_home(df)

    work = detect_work(df, home)

    memory = update_memory(df)

    learned_home = get_best_home(memory)

    learned_work = get_best_work(memory)

    if learned_home:
        home = learned_home

    if learned_work:
        work = learned_work

    print("🏠 LEARNED HOME:", home)

    print("🏢 LEARNED WORK:", work)

    # =================================================
    # CLAIMS
    # =================================================

    df["Claim (ZAR)"] = (
        df["KM"] * RATE_PER_KM
    ).round(2)

    df["Month"] = pd.to_datetime(
        df["Date"]
    ).dt.strftime("%B")

    summary = df.groupby("Month").agg({
        "KM": "sum",
        "Claim (ZAR)": "sum"
    }).reset_index()

    purpose_df = df.groupby("Purpose").agg({
        "KM": "sum"
    }).reset_index()

    review_df = build_review_queue(df)

    audit_summary_df = build_audit_summary(
        df,
        home,
        work
    )

    # =================================================
    # CLEAN TIMEZONE
    # =================================================

    df["Start Time"] = (
        df["Start Time"]
        .dt.tz_convert(None)
    )

    df["End Time"] = (
        df["End Time"]
        .dt.tz_convert(None)
    )

    # =================================================
    # EXPORT FILES
    # =================================================

    os.makedirs(
        "backend/exports",
        exist_ok=True
    )

    print("📄 Writing Excel file...")

    with pd.ExcelWriter(
        OUTPUT_FILE,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Trips",
            index=False
        )

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        purpose_df.to_excel(
            writer,
            sheet_name="Purposes",
            index=False
        )

        review_df.to_excel(
            writer,
            sheet_name="Review Queue",
            index=False
        )

        audit_summary_df.to_excel(
            writer,
            sheet_name="Audit Summary",
            index=False
        )

    total_km = round(df["KM"].sum(), 2)

    business_km = round(
        df[df["Trip Type"] == "Business"]["KM"].sum(),
        2
    )

    estimated_claim = round(
        business_km * RATE_PER_KM,
        2
    )

    generate_pdf_report(
        output_path=PDF_OUTPUT,
        tax_year=TAX_YEAR,
        home=home,
        total_km=total_km,
        business_km=business_km,
        estimated_claim=estimated_claim,
        summary_df=summary,
        purpose_df=purpose_df
    )

    print("\n====================================")
    print("✅ EXPORT COMPLETE")
    print("====================================")

    print("Trips:", len(df))

    print("Total KM:", total_km)

    print("Business KM:", business_km)

    print("Claim:", estimated_claim)


# =================================================
# RUN
# =================================================

if __name__ == "__main__":

    parse_timeline()