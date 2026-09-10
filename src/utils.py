"""
utils.py
--------
Shared utility functions used across the analysis and dashboard modules.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_student_data.csv")
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "student_placement_data.csv")
VIS_DIR = os.path.join(BASE_DIR, "visualizations")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

CGPA_BINS = [0, 6, 7, 8, 9, 10.001]
CGPA_LABELS = ["Below 6", "6 to 7", "7 to 8", "8 to 9", "Above 9"]


def load_clean_data(path=CLEAN_DATA_PATH):
    """Load the cleaned dataset with basic error handling. Returns a
    DataFrame, or raises a clear, user-friendly exception."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Cleaned dataset not found at '{path}'. "
            "Please run 'python src/data_generator.py' and "
            "'python src/data_cleaning.py' first."
        )
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("The dataset is empty.")
    return df


def add_cgpa_range(df):
    """Add a CGPA_Range categorical column to the dataframe."""
    df = df.copy()
    df["CGPA_Range"] = pd.cut(df["CGPA"], bins=CGPA_BINS, labels=CGPA_LABELS, right=False)
    return df


def placement_rate(df):
    if len(df) == 0:
        return 0.0
    return (df["Placement_Status"] == "Placed").mean() * 100


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path
