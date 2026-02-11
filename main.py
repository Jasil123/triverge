import csv
import re
import os
from openpyxl import Workbook

# ====== FOLDERS ======
INPUT_FOLDER = "documents"
OUTPUT_FOLDER = "output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

KEEP_COLUMNS = [
    "Submitted at",
    "Name",
    "College Name",
    "Department",
    "e-mail",
    "Phone Number"
]

def extract_event_name(col_name):
    match = re.search(r"\((.*?)\)", col_name)
    return match.group(1).strip() if match else col_name

def convert_csv_to_excel(input_path, output_path):
    print(f"Processing: {input_path}")

    # -------- READ CSV --------
    with open(input_path, newline="", encoding="utf-8-sig") as infile:
        reader = csv.DictReader(infile)

        raw_headers = reader.fieldnames
        headers = [h.strip() for h in raw_headers]

        rows = []
        for row in reader:
            clean_row = {}
            for k, v in row.items():
                clean_row[k.strip()] = v.strip() if v else ""
            rows.append(clean_row)

    # Detect checkbox event columns
    event_columns = [
        h for h in headers
        if h.startswith("Events") and "(" in h and ")" in h
    ]

    # -------- CREATE EXCEL --------
    wb = Workbook()
    ws = wb.active
    ws.title = "Submissions"

    final_headers = KEEP_COLUMNS + ["Selected Options"]
    ws.append(final_headers)

    # Write rows
    for row in rows:
        selected_events = []

        for col in event_columns:
            if row.get(col, "").upper() == "TRUE":
                selected_events.append(extract_event_name(col))

        ws.append([
            row.get("Submitted at", ""),
            row.get("Name", ""),
            row.get("College Name", ""),
            row.get("Department", ""),
            row.get("e-mail", ""),
            row.get("Phone Number", ""),
            ", ".join(selected_events)
        ])

    # -------- AUTO FIT WIDTH --------
    for column_cells in ws.columns:
        max_length = 0
        column_letter = column_cells[0].column_letter
        
        for cell in column_cells:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        ws.column_dimensions[column_letter].width = max_length + 3

    wb.save(output_path)
    print(f"✅ Saved: {output_path}\n")


# ====== LOOP THROUGH ALL CSV FILES ======
for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith(".csv"):
        input_file = os.path.join(INPUT_FOLDER, filename)

        # change extension to xlsx
        output_name = filename.replace(".csv", ".xlsx")
        output_file = os.path.join(OUTPUT_FOLDER, output_name)

        convert_csv_to_excel(input_file, output_file)

print("🎉 All CSV files converted successfully!")
