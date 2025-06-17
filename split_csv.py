import os
import pandas as pd

# === CONFIGURATION ===
INPUT_CSV = "grade_distr_SUM2022_FALL2024_FINAL.csv"
OUTPUT_DIR = "split_by_term"

# === Step 1: Define expected column names (in order) ===
expected_columns = [
    "TERM", "SUBJECT", "CATALOG NBR", "CLASS SECTION", "CLASS NUMBER",
    "COURSE DESCR", "INSTR LAST NAME", "INSTR FIRST NAME",
    "A", "B", "C", "D", "F",
    "SATISFACTORY", "NOT REPORTED", "TOTAL DROPPED", "AVG GPA"
]

# === Step 2: Read and clean original CSV ===
df = pd.read_csv(INPUT_CSV)

# Mapping of incorrect column names to correct ones
column_renames = {
    "CATALOG_NBR": "CATALOG NBR",
    "CLASS_SECTION": "CLASS SECTION",
    "CLASS_NUMBER": "CLASS NUMBER",
    "COURSE_DESCR": "COURSE DESCR",
    "INSTR_LAST_NAME": "INSTR LAST NAME",
    "INSTR_FIRST_NAME": "INSTR FIRST NAME",
    "SASTISFACTORY": "SATISFACTORY",  # fix typo, haha
    "NOT_REPORTED": "NOT REPORTED",
    "TOTAL_DROPPED": "TOTAL DROPPED",
    "AVG_GPA": "AVG GPA"
}

# Rename columns
df.rename(columns=column_renames, inplace=True)

# Remove missing columns from expected list
valid_columns = [col for col in expected_columns if col in df.columns]
df = df[valid_columns]

# === Step 3: Output Directory ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Step 4: Mapping for season codes ===
season_code = {"Spring": "01", "Summer": "02", "Fall": "03"}

# === Step 5: Split and save files ===
for term in df['TERM'].dropna().unique():
    try:
        season, year = term.split()
        code = season_code[season]
        filename = f"Grade Distribution {year}-{code} ({season} {year}).csv"
        path = os.path.join(OUTPUT_DIR, filename)
        df[df['TERM'] == term].to_csv(path, index=False)
    except Exception as e:
        print(f"Error processing term '{term}': {e}")

print("All CSVs saved using official naming format in:", os.path.abspath(OUTPUT_DIR))
