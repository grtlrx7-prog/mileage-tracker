def parse_timeline():

    print("SCRIPT STARTED...")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("semanticSegments", [])

    print(f"Segments loaded: {len(segments)}")

    rows = []

    print("Starting segment parsing...")

    for i, s in enumerate(segments):

        # ============================================
        # DEBUG HEARTBEAT (PROVES IT IS STILL RUNNING)
        # ============================================
        if i % 100 == 0:
            print(f"Heartbeat → Processing segment {i}/{len(segments)}")

        act = s.get("activity", {})
        start = s.get("startTime")
        end = s.get("endTime")

        if not start or not end:
            continue

        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)

        distance = act.get("distanceMeters", 0)

        if distance <= 0:
            continue

        km = round(distance / 1000, 2)

        if km < 1:
            continue

        # ============================================
        # ADDRESS LOOKUPS (DEBUGGED)
        # ============================================

        print("Fetching FROM address...")
        from_addr = get_address(act.get("start", {}).get("latLng"))

        print("Fetching TO address...")
        to_addr = get_address(act.get("end", {}).get("latLng"))

        rows.append({
            "Date": start_dt.date(),
            "Start Time": start_dt.tz_localize(None),
            "End Time": end_dt.tz_localize(None),
            "Duration (min)": round((end_dt - start_dt).total_seconds() / 60, 1),
            "From": from_addr,
            "To": to_addr,
            "KM": km
        })

    print(f"Raw trips built: {len(rows)}")

    df = pd.DataFrame(rows)

    if df.empty:
        print("No trips found")
        return

    df = merge_trips(df)

    home = detect_home(df)
    print("HOME:", home)

    df["Trip Type"] = df.apply(lambda r: classify_trip(r["From"], r["To"], home), axis=1)
    df["Purpose"] = df.apply(classify_purpose, axis=1)

    df["Claim (ZAR)"] = (df["KM"] * RATE_PER_KM).round(2)

    df["Month"] = pd.to_datetime(df["Date"]).dt.strftime("%B")

    summary = df.groupby("Month").agg({
        "KM": "sum",
        "Claim (ZAR)": "sum"
    }).reset_index()

    purpose_df = df.groupby("Purpose").agg({
        "KM": "sum",
        "Purpose": "count"
    }).rename(columns={"Purpose": "Trips"}).reset_index()

    # ============================================
    # EXCEL EXPORT
    # ============================================

    print("Writing Excel file...")

    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:

        df.to_excel(writer, sheet_name="Trips", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)

        ws = writer.sheets["Trips"]

        header_fill = PatternFill("solid", fgColor="1F4E78")
        header_font = Font(bold=True, color="FFFFFF")

        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")

        for col in ws.columns:
            max_len = max(len(str(c.value)) if c.value else 0 for c in col)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 5, 45)

        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

    # ============================================
    # CACHE SAVE
    # ============================================

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(address_cache, f, indent=2)

    # ============================================
    # PDF EXPORT
    # ============================================

    total_km = df["KM"].sum()
    business_km = df[df["Trip Type"] == "Business"]["KM"].sum()

    try:
        generate_pdf_report(
            output_path=PDF_OUTPUT,
            tax_year=TAX_YEAR,
            home=home,
            total_km=total_km,
            business_km=business_km,
            estimated_claim=business_km * RATE_PER_KM,
            summary_df=summary,
            purpose_df=purpose_df
        )
        print("PDF Saved:", PDF_OUTPUT)

    except Exception as e:
        print("PDF failed:", e)

    # ============================================
    # OUTPUT
    # ============================================

    print("\n====================================")
    print("EXPORT COMPLETE")
    print("====================================")

    print(f"Trips: {len(df)}")
    print(f"Total KM: {total_km:.2f}")
    print(f"Business KM: {business_km:.2f}")
    print(f"Estimated Claim: R{business_km * RATE_PER_KM:.2f}")

    print("\nExcel Saved:", OUTPUT_FILE)