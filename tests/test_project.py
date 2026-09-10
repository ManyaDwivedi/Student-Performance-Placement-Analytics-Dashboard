"""
test_project.py
----------------
Basic tests for the Student Performance & Placement Analytics project.

Run:
    python tests/test_project.py

or with pytest:
    pytest tests/test_project.py -v
"""

import os
import sys
import unittest

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


class TestDatasetExistence(unittest.TestCase):

    def test_raw_dataset_exists(self):
        self.assertTrue(os.path.exists(RAW_PATH), "Raw dataset file is missing.")

    def test_cleaned_dataset_exists(self):
        self.assertTrue(os.path.exists(CLEAN_PATH), "Cleaned dataset file is missing.")


class TestDatasetIntegrity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(CLEAN_PATH):
            cls.df = pd.read_csv(CLEAN_PATH)
        else:
            cls.df = None

    def test_dataset_not_empty(self):
        self.assertIsNotNone(self.df, "Cleaned dataset could not be loaded.")
        self.assertGreater(len(self.df), 0, "Dataset is empty.")

    def test_required_columns_exist(self):
        self.assertIsNotNone(self.df)
        missing = [c for c in REQUIRED_COLUMNS if c not in self.df.columns]
        self.assertEqual(missing, [], f"Missing columns: {missing}")

    def test_no_duplicate_student_ids(self):
        self.assertIsNotNone(self.df)
        self.assertEqual(
            self.df["Student_ID"].duplicated().sum(), 0,
            "Duplicate Student_ID values found."
        )

    def test_cgpa_values_valid(self):
        self.assertIsNotNone(self.df)
        self.assertTrue((self.df["CGPA"] >= 0).all() and (self.df["CGPA"] <= 10).all(),
                         "CGPA values out of valid range [0, 10].")

    def test_attendance_values_valid(self):
        self.assertIsNotNone(self.df)
        self.assertTrue(
            (self.df["Attendance_Percentage"] >= 0).all()
            and (self.df["Attendance_Percentage"] <= 100).all(),
            "Attendance values out of valid range [0, 100].",
        )

    def test_scores_valid(self):
        self.assertIsNotNone(self.df)
        for col in ["Aptitude_Score", "Communication_Score"]:
            self.assertTrue(
                (self.df[col] >= 0).all() and (self.df[col] <= 100).all(),
                f"{col} values out of valid range [0, 100].",
            )

    def test_salary_values_valid(self):
        self.assertIsNotNone(self.df)
        self.assertTrue((self.df["Salary_Package_LPA"] >= 0).all(),
                         "Negative salary values found.")

    def test_placement_logic_valid(self):
        self.assertIsNotNone(self.df)
        not_placed = self.df[self.df["Placement_Status"] == "Not Placed"]
        self.assertTrue((not_placed["Company"] == "Not Applicable").all(),
                         "Not Placed students should have Company = 'Not Applicable'.")
        self.assertTrue((not_placed["Salary_Package_LPA"] == 0).all(),
                         "Not Placed students should have Salary_Package_LPA = 0.")

    def test_placement_status_values(self):
        self.assertIsNotNone(self.df)
        valid_statuses = {"Placed", "Not Placed"}
        self.assertTrue(set(self.df["Placement_Status"].unique()).issubset(valid_statuses),
                         "Unexpected values found in Placement_Status column.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
