import os
import re
import pandas as pd
from collections import Counter

# Set base directory
BASE_DIR = os.getcwd()
output_file = os.path.join(BASE_DIR, "mi_grade_summary.xlsx")

def parse_mi_file(file_path):
    grades = []
    try:
        with open(file_path, 'r', encoding='utf-16', errors='ignore') as f:
            for line in f:
                parts = line.strip().rsplit("-", maxsplit=1)
                if len(parts) == 2:
                    grade = parts[1].strip()
                    if grade in ["A", "B", "C", "D", "E", "F"]:
                        grades.append(grade)
    except Exception as e:
        print(f"[ERROR] Could not parse {file_path}: {e}")
    return grades

mi_data = {}

# Walk through all subfolders and files
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith("_mi.txt"):
            project = os.path.basename(root)
            full_path = os.path.join(root, file)
            grades = parse_mi_file(full_path)

            if grades:
                count = Counter(grades)
                df = pd.DataFrame(count.items(), columns=["Grade", "Count"]).sort_values(by="Grade")
                mi_data[project] = df
                print(f"[OK] Parsed {project} - Grades: {dict(count)}")
            else:
                print(f"[SKIP] No grades found in: {file}")

# Write results to Excel
if mi_data:
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        for project, df in mi_data.items():
            sheet_name = project[:31]  # Excel limit
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"\nMI grade summary saved to: {output_file}")
else:
    print("\nNo MI data parsed. Please check encoding or file format.")
