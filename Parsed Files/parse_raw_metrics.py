import os
import re
import pandas as pd

BASE_DIR = os.getcwd()
output_file = os.path.join(BASE_DIR, "raw_metrics_summary.xlsx")

def parse_raw_metrics(file_path):
    metrics = {
        "LOC": 0,
        "LLOC": 0,
        "SLOC": 0,
        "Comments": 0,
        "Single_comments": 0,
        "Multi": 0,
        "Blank": 0,
        "C%L": 0.0,
        "C%S": 0.0,
        "C+M%L": 0.0
    }

    with open(file_path, 'r', encoding='utf-16', errors='ignore') as f:
        for line in f:
            line = line.strip()

            if "LOC:" in line:
                match = re.search(r'LOC:\s*(\d+)', line)
                if match:
                    metrics["LOC"] += int(match.group(1))

            if "LLOC:" in line:
                match = re.search(r'LLOC:\s*(\d+)', line)
                if match:
                    metrics["LLOC"] += int(match.group(1))

            if "SLOC:" in line:
                match = re.search(r'SLOC:\s*(\d+)', line)
                if match:
                    metrics["SLOC"] += int(match.group(1))

            if "Comments:" in line:
                match = re.search(r'Comments:\s*(\d+)', line)
                if match:
                    metrics["Comments"] += int(match.group(1))

            if "Single comments:" in line:
                match = re.search(r'Single comments:\s*(\d+)', line)
                if match:
                    metrics["Single_comments"] += int(match.group(1))

            if "Multi:" in line:
                match = re.search(r'Multi:\s*(\d+)', line)
                if match:
                    metrics["Multi"] += int(match.group(1))

            if "Blank:" in line:
                match = re.search(r'Blank:\s*(\d+)', line)
                if match:
                    metrics["Blank"] += int(match.group(1))

            if "(C % L):" in line:
                match = re.search(r'\(C % L\):\s*([0-9]+)%', line)
                if match:
                    metrics["C%L"] += int(match.group(1))

            if "(C % S):" in line:
                match = re.search(r'\(C % S\):\s*([0-9]+)%', line)
                if match:
                    metrics["C%S"] += int(match.group(1))

            if "(C + M % L):" in line:
                match = re.search(r'\(C \+ M % L\):\s*([0-9]+)%', line)
                if match:
                    metrics["C+M%L"] += int(match.group(1))

    return metrics

# Walk through all subfolders and collect results
raw_results = []

for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith("_raw.txt"):
            project = os.path.basename(root)
            full_path = os.path.join(root, file)
            raw_metrics = parse_raw_metrics(full_path)
            raw_metrics["Project"] = project
            raw_results.append(raw_metrics)
            print(f"[OK] Parsed raw metrics for: {project}")

# Write to Excel
if raw_results:
    df = pd.DataFrame(raw_results)
    df = df[["Project", "LOC", "LLOC", "SLOC", "Comments", "Single_comments", "Multi", "Blank", "C%L", "C%S", "C+M%L"]]
    df.to_excel(output_file, index=False)
    print(f"\n✅ Raw metrics summary saved to: {output_file}")
else:
    print("\n❌ No raw metrics found.")
