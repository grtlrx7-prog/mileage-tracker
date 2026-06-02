import os
import datetime
import shutil

from backend.parsers.sars_export import parse_timeline


# =================================================
# AUTO SARS EXPORT RUNNER
# =================================================

def run_export():

    print("\n====================================")
    print("AUTO SARS EXPORT STARTING")
    print("====================================")

    # =========================================
    # CREATE TAX YEAR FOLDER
    # =========================================

    year = datetime.datetime.now().year

    tax_folder = f"backend/exports/{year}_SARS_PACK"

    os.makedirs(tax_folder, exist_ok=True)

    print(f"Output folder: {tax_folder}")

    # =========================================
    # RUN MAIN PIPELINE
    # =========================================

    parse_timeline()

    # =========================================
    # MOVE FILES INTO PACK
    # =========================================

    files = [
        "backend/exports/mileage_logbook.xlsx",
        "backend/exports/sars_audit_report.pdf"
    ]

    for file in files:

        if os.path.exists(file):

            shutil.copy(file, tax_folder)

    # =========================================
    # CREATE SIMPLE INDEX FILE
    # =========================================

    index_file = os.path.join(tax_folder, "README.txt")

    with open(index_file, "w") as f:

        f.write("SARS EXPORT PACK\n")
        f.write("=================\n\n")
        f.write("Contains:\n")
        f.write("- Mileage Logbook (Excel)\n")
        f.write("- SARS Audit Report (PDF)\n\n")
        f.write("Generated automatically by system.\n")

    # =========================================
    # COMPLETE
    # =========================================

    print("\n====================================")
    print("EXPORT PACK COMPLETE")
    print("====================================")
    print(f"Saved to: {tax_folder}\n")


# =================================================
# ENTRY
# =================================================

if __name__ == "__main__":
    run_export()