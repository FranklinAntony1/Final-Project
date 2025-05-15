import os
import re
import pandas as pd

BASE_DIR = os.getcwd()
output_file = os.path.join(BASE_DIR, "cc_detailed_summary.xlsx")

def parse_function_complexities(file_path):
    complexities = []
    with open(file_path, 'r', encoding='utf-16', errors='ignore') as f:
        for line in f:
            match = re.search(r'\(([0-9]+)\)', line.strip())
            if match:
                complexities.append(int(match.group(1)))
    return complexities


results = []

for root, dirs, files in os.walk(BASE_DIR):
    cc_file = None
    project = os.path.basename(root)

    if f"{project}_cc_funcs.txt" in files:
        cc_file = os.path.join(root, f"{project}_cc_funcs.txt")
    elif f"{project}_cc.txt" in files:
        cc_file = os.path.join(root, f"{project}_cc.txt")

    if cc_file:
        scores = parse_function_complexities(cc_file)
        if scores:
            result = {
                "Project": project,
                "Functions_Analyzed": len(scores),
                "Average_Complexity": round(sum(scores) / len(scores), 2),
                "Max_Complexity": max(scores),
                "Functions_>10_CC": sum(1 for x in scores if x > 10)
            }
            results.append(result)
            print(f"[OK] {project} - {len(scores)} functions")
        else:
            print(f"[SKIP] {project} - No complexity data found")

if results:
    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)
    print(f"\n✅ Detailed CC summary saved to: {output_file}")
else:
    print("\n❌ No CC data extracted.")
