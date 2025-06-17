import os
import pandas as pd

# === CONFIGURATION ===
INPUT_CSV = "grade_distr_SUM2022_FALL2024_FINAL.csv" 
OUTPUT_DIR = "split_by_term"  # Where to store the split CSVs

# === STEP 1: Load the CSV ===
df = pd.read_csv(INPUT_CSV)

# === STEP 2: Ensure TERM column exists ===
if 'TERM' not in df.columns:
	raise ValueError("CSV is missing 'TERM' column, required for term splitting.")

# === STEP 3: Prepare output directory ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === STEP 4: Split and save ===
for term in df['TERM'].unique():
	year, season = term.split()
	output_filename = f"{year}_{season}.csv"
	output_path = os.path.join(OUTPUT_DIR, output_filename)
	df[df['TERM'] == term].to_csv(output_path, index=False)

print("CSV split complete.")
print(f"Files saved to: {os.path.abspath(OUTPUT_DIR)}")
