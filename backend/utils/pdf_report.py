from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


# =================================================
# SARS PROFESSIONAL AUDIT PDF REPORT
# =================================================

def generate_pdf_report(
    output_path,
    tax_year,
    home,
    total_km,
    business_km,
    estimated_claim,
    summary_df,
    purpose_df
):

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    content = []

    # =================================================
    # TITLE
    # =================================================

    content.append(Paragraph(
        "SARS VEHICLE TRAVEL LOGBOOK AUDIT REPORT",
        styles["Title"]
    ))

    content.append(Spacer(1, 12))

    # =================================================
    # DECLARATION
    # =================================================

    declaration = f"""
    This report summarises vehicle travel activity for the tax year {tax_year}.
    The data has been automatically generated from GPS movement logs and processed
    into structured business, personal, and commuting travel categories.
    """

    content.append(Paragraph(declaration, styles["Normal"]))
    content.append(Spacer(1, 12))

    # =================================================
    # SUMMARY SECTION
    # =================================================

    summary_data = [
        ["Home Location", home],
        ["Total Distance (KM)", str(round(total_km, 2))],
        ["Business Distance (KM)", str(round(business_km, 2))],
        ["Estimated Claim (ZAR)", f"R{round(estimated_claim, 2)}"]
    ]

    summary_table = Table(summary_data)

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    content.append(summary_table)
    content.append(Spacer(1, 20))

    # =================================================
    # PURPOSE BREAKDOWN
    # =================================================

    content.append(Paragraph("TRIP PURPOSE BREAKDOWN", styles["Heading2"]))
    content.append(Spacer(1, 10))

    purpose_table_data = [["Purpose", "KM"]]

    for _, row in purpose_df.iterrows():
        purpose_table_data.append([
            str(row["Purpose"]),
            str(round(row["KM"], 2))
        ])

    purpose_table = Table(purpose_table_data)

    purpose_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ]))

    content.append(purpose_table)
    content.append(Spacer(1, 20))

    # =================================================
    # MONTHLY SUMMARY
    # =================================================

    content.append(Paragraph("MONTHLY TRAVEL SUMMARY", styles["Heading2"]))
    content.append(Spacer(1, 10))

    monthly_table_data = [["Month", "KM", "Claim (ZAR)"]]

    for _, row in summary_df.iterrows():
        monthly_table_data.append([
            str(row["Month"]),
            str(round(row["KM"], 2)),
            f"R{round(row['Claim (ZAR)'], 2)}"
        ])

    monthly_table = Table(monthly_table_data)

    monthly_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ]))

    content.append(monthly_table)
    content.append(Spacer(1, 20))

    # =================================================
    # SARS DECLARATION
    # =================================================

    declaration_text = """
    DECLARATION:
    This logbook is generated from GPS movement data and represents a true
    reflection of vehicle usage for the selected tax year.

    All trips are classified into Business, Personal, or Commute categories
    based on location patterns and travel behavior analysis.

    This document is intended for submission to the South African Revenue Service (SARS)
    as supporting evidence for travel deduction claims.
    """

    content.append(Paragraph(declaration_text, styles["Normal"]))

    # =================================================
    # BUILD PDF
    # =================================================

    doc.build(content)