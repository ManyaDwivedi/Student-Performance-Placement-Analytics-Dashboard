"""
data_cleaning.py
-----------------
Loads the raw student placement dataset, validates and cleans it, and
saves a clean version ready for analysis.

Run:
    python src/data_cleaning.py
"""

import os
import sys
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "student_placement_data.csv")
CLEAN_PATH = os.path.join(BASE_DIR, "data", "cleaned_student_data.csv")

REQUIRED_COLUMNS = [
    "Student_ID", "Student_Name", "Gender", "Age", "Branch", "CGPA",
    "Attendance_Percentage", "Technical_Skills", "Internships", "Projects",
    "Certifications", "Aptitude_Score", "Communication_Score",
    "Placement_Status", "Company", "Salary_Package_LPA",
]


def load_data(path):
    if not os.path.exists(path):
        print(f"ERROR: Dataset not found at '{path}'.")
        print("Please run 'python src/data_generator.py' first.")
        sys.exit(1)
    try:
        df = pd.read_csv(path)
    except Exception as exc:
        print(f"ERROR: Failed to read dataset - {exc}")
        sys.exit(1)
    if df.empty:
        print("ERROR: Dataset is empty.")
        sys.exit(1)
    return df


def validate_columns(df):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        print(f"ERROR: Missing required columns: {missing}")
        sys.exit(1)


def clean_dataset(df):
    summary = {}

    summary["initial_shape"] = df.shape

    # Duplicates
    dup_count = df.duplicated().sum()
    summary["duplicates_found"] = int(dup_count)
    if dup_count > 0:
        df = df.drop_duplicates()

    # Missing values
    missing_before = df.isnull().sum()
    summary["missing_before"] = missing_before[missing_before > 0].to_dict()

    # Handle missing numeric values with median, categorical with mode
    numeric_cols = [
        "Age", "CGPA", "Attendance_Percentage", "Technical_Skills",
        "Internships", "Projects", "Certifications", "Aptitude_Score",
        "Communication_Score", "Salary_Package_LPA",
    ]
    categorical_cols = ["Gender", "Branch", "Placement_Status", "Company", "Student_Name"]

    for col in numeric_cols:
        if col in df.columns and df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    for col in categorical_cols:
        if col in df.columns and df[col].isnull().any():
            mode_val = df[col].mode()
            fill_val = mode_val.iloc[0] if not mode_val.empty else "Unknown"
            df[col] = df[col].fillna(fill_val)

    # Validate CGPA range (0-10)
    invalid_cgpa = ((df["CGPA"] < 0) | (df["CGPA"] > 10)).sum()
    summary["invalid_cgpa_clipped"] = int(invalid_cgpa)
    df["CGPA"] = df["CGPA"].clip(0, 10)

    # Validate Attendance range (0-100)
    invalid_att = ((df["Attendance_Percentage"] < 0) | (df["Attendance_Percentage"] > 100)).sum()
    summary["invalid_attendance_clipped"] = int(invalid_att)
    df["Attendance_Percentage"] = df["Attendance_Percentage"].clip(0, 100)

    # Validate scores (0-100)
    for score_col in ["Aptitude_Score", "Communication_Score"]:
        invalid_score = ((df[score_col] < 0) | (df[score_col] > 100)).sum()
        summary[f"invalid_{score_col.lower()}_clipped"] = int(invalid_score)
        df[score_col] = df[score_col].clip(0, 100)

    # Validate Salary (non-negative)
    invalid_salary = (df["Salary_Package_LPA"] < 0).sum()
    summary["invalid_salary_clipped"] = int(invalid_salary)
    df["Salary_Package_LPA"] = df["Salary_Package_LPA"].clip(lower=0)

    # Validate placement logic consistency
    not_placed_mask = df["Placement_Status"] == "Not Placed"
    inconsistent = (
        (not_placed_mask & (df["Company"] != "Not Applicable"))
        | (not_placed_mask & (df["Salary_Package_LPA"] != 0))
    ).sum()
    summary["placement_logic_fixed"] = int(inconsistent)
    df.loc[not_placed_mask, "Company"] = "Not Applicable"
    df.loc[not_placed_mask, "Salary_Package_LPA"] = 0.0

    summary["final_shape"] = df.shape
    return df, summary


def print_summary(df, summary):
    print("=" * 70)
    print("STUDENT PERFORMANCE & PLACEMENT ANALYTICS - DATA CLEANING")
    print("=" * 70)

    print(f"\nDataset dimensions (before cleaning): {summary['initial_shape']}")
    print("\nFirst 5 records:")
    print(df.head(5).to_string(index=False))

    print("\nColumn names:")
    print(list(df.columns))

    print("\nData types:")
    print(df.dtypes)

    print(f"\nDuplicate records found and removed: {summary['duplicates_found']}")

    if summary["missing_before"]:
        print(f"\nMissing values found (before fill): {summary['missing_before']}")
    else:
        print("\nMissing values found: None")

    print(f"\nInvalid CGPA values clipped to [0, 10]: {summary['invalid_cgpa_clipped']}")
    print(f"Invalid Attendance values clipped to [0, 100]: {summary['invalid_attendance_clipped']}")
    print(f"Invalid Aptitude Score values clipped: {summary['invalid_aptitude_score_clipped']}")
    print(f"Invalid Communication Score values clipped: {summary['invalid_communication_score_clipped']}")
    print(f"Invalid (negative) Salary values clipped: {summary['invalid_salary_clipped']}")
    print(f"Placement logic inconsistencies fixed: {summary['placement_logic_fixed']}")

    print(f"\nFinal dataset dimensions: {summary['final_shape']}")
    print("\nCleaning summary: Dataset validated and cleaned successfully.")


def main():
    df = load_data(RAW_PATH)
    validate_columns(df)
    cleaned_df, summary = clean_dataset(df)

    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
    cleaned_df.to_csv(CLEAN_PATH, index=False)

    print_summary(cleaned_df, summary)
    print(f"\nCleaned dataset saved to: {CLEAN_PATH}")


if __name__ == "__main__":
    main()
