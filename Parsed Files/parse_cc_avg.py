import os
import re
import pandas as pd

# Set base directory
BASE_DIR = os.getcwd()
output_file = os.path.join(BASE_DIR, "cc_avg_summary.xlsx")

def extract_avg_complexity(file_path):
    try:
        with open(file_path, 'r', encoding='utf-16', errors='ignore') as f:
            text = f.read()
            match = re.search(r'Average complexity:\s*[A-F]\s*\(([\d.]+)\)', text)
            if match:
                return float(match.group(1))
    except Exception as e:
        print(f"[ERROR] Failed to parse {file_path}: {e}")
    return None


# Dictionary to store results
cc_results = []

# Recursively look for *_cc_avg.txt files
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith("_cc_avg.txt"):
            project = os.path.basename(root)
            path = os.path.join(root, file)
            avg_cc = extract_avg_complexity(path)

            if avg_cc is not None:
                cc_results.append({"Project": project, "Average_CC": avg_cc})
                print(f"[OK] {project} - Average CC: {avg_cc}")
            else:
                print(f"[SKIP] No CC value found in {file}")

# Save to Excel
if cc_results:
    df = pd.DataFrame(cc_results)
    df.to_excel(output_file, index=False)
    print(f"\n✅ Cyclomatic complexity summary saved to: {output_file}")
else:
    print("\n❌ No cyclomatic complexity data found.")
