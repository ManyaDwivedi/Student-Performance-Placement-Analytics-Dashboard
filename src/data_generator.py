"""
data_generator.py
------------------
Generates a realistic synthetic dataset of student academic performance
and placement outcomes for the Student Performance & Placement Analytics
project.

Run:
    python src/data_generator.py
"""

import os
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
np.random.seed(42)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
NUM_STUDENTS = 800

BRANCHES = [
    "Computer Science Engineering",
    "Artificial Intelligence & Machine Learning",
    "Information Technology",
    "Electronics & Communication",
    "Mechanical Engineering",
    "Civil Engineering",
]
BRANCH_WEIGHTS = [0.22, 0.18, 0.18, 0.16, 0.14, 0.12]

GENDERS = ["Male", "Female", "Other"]
GENDER_WEIGHTS = [0.56, 0.42, 0.02]

COMPANIES = [
    "TCS", "Infosys", "Wipro", "Accenture", "Deloitte",
    "Capgemini", "Cognizant", "HCLTech", "Tech Mahindra", "IBM",
]

FIRST_NAMES_MALE = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Reyansh", "Krishna",
    "Ishaan", "Rohan", "Kabir", "Aryan", "Dhruv", "Karan", "Sameer",
    "Yash", "Rahul", "Nikhil", "Manav", "Siddharth", "Harsh",
]
FIRST_NAMES_FEMALE = [
    "Ananya", "Diya", "Ishita", "Saanvi", "Aadhya", "Myra", "Anika",
    "Riya", "Kavya", "Priya", "Sneha", "Pooja", "Neha", "Tanvi",
    "Aditi", "Meera", "Shreya", "Simran", "Nisha", "Kritika",
]
FIRST_NAMES_OTHER = ["Alex", "Sam", "Rey", "Noor", "Kai", "Ari"]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Patel", "Mehta",
    "Joshi", "Reddy", "Nair", "Iyer", "Yadav", "Chauhan", "Malhotra",
    "Kapoor", "Agarwal", "Bansal", "Chatterjee", "Mishra", "Tripathi",
    "Dwivedi", "Rao", "Pandey", "Saxena", "Bhatt",
]


def generate_names(n_students, genders):
    """Generate realistic fictional student names based on gender."""
    names = []
    for g in genders:
        if g == "Male":
            first = np.random.choice(FIRST_NAMES_MALE)
        elif g == "Female":
            first = np.random.choice(FIRST_NAMES_FEMALE)
        else:
            first = np.random.choice(FIRST_NAMES_OTHER)
        last = np.random.choice(LAST_NAMES)
        names.append(f"{first} {last}")
    return names


def generate_dataset(n=NUM_STUDENTS):
    """Generate the full synthetic student dataset with realistic
    relationships between academic/skill features and placement outcome."""

    student_ids = [f"STU{str(i).zfill(3)}" for i in range(1, n + 1)]

    gender = np.random.choice(GENDERS, size=n, p=GENDER_WEIGHTS)
    student_name = generate_names(n, gender)
    age = np.random.randint(20, 26, size=n)
    branch = np.random.choice(BRANCHES, size=n, p=BRANCH_WEIGHTS)

    cgpa = np.round(np.clip(np.random.normal(7.4, 1.0, n), 5.0, 10.0), 2)
    attendance = np.round(np.clip(np.random.normal(80, 12, n), 50, 100), 1)
    technical_skills = np.clip(
        np.random.normal(5.5, 2.0, n).round().astype(int), 1, 10
    )
    internships = np.clip(
        np.random.poisson(1.1, n), 0, 4
    )
    projects = np.clip(
        np.random.poisson(3.0, n), 0, 8
    )
    certifications = np.clip(
        np.random.poisson(2.5, n), 0, 10
    )
    aptitude_score = np.round(np.clip(np.random.normal(62, 18, n), 0, 100), 1)
    communication_score = np.round(np.clip(np.random.normal(65, 15, n), 0, 100), 1)

    # ------------------------------------------------------------------
    # Placement probability model (weighted, realistic, with noise)
    # ------------------------------------------------------------------
    def norm(x, lo, hi):
        return np.clip((x - lo) / (hi - lo), 0, 1)

    score = (
        0.28 * norm(cgpa, 5.0, 10.0)
        + 0.12 * norm(attendance, 50, 100)
        + 0.14 * norm(technical_skills, 1, 10)
        + 0.16 * norm(internships, 0, 4)
        + 0.10 * norm(projects, 0, 8)
        + 0.08 * norm(certifications, 0, 10)
        + 0.06 * norm(aptitude_score, 0, 100)
        + 0.06 * norm(communication_score, 0, 100)
    )

    # add randomness so outcomes are not perfectly predictable
    noise = np.random.normal(0, 0.14, n)
    final_score = score + noise

    # Convert score to placement probability via logistic-like curve
    prob = 1 / (1 + np.exp(-8 * (final_score - 0.52)))
    placement_status = np.where(
        np.random.rand(n) < prob, "Placed", "Not Placed"
    )

    company = []
    salary_package = []
    for i in range(n):
        if placement_status[i] == "Placed":
            company.append(np.random.choice(COMPANIES))
            # salary logically depends on cgpa, internships, projects,
            # technical skills, aptitude, communication
            base = (
                2.5
                + 1.0 * (cgpa[i] - 5.0)
                + 0.6 * internships[i]
                + 0.25 * projects[i]
                + 0.25 * technical_skills[i]
                + 0.02 * aptitude_score[i]
                + 0.015 * communication_score[i]
            )
            base += np.random.normal(0, 1.6)
            salary = float(np.clip(base, 3.0, 20.0))
            salary_package.append(round(salary, 2))
        else:
            company.append("Not Applicable")
            salary_package.append(0.0)

    df = pd.DataFrame(
        {
            "Student_ID": student_ids,
            "Student_Name": student_name,
            "Gender": gender,
            "Age": age,
            "Branch": branch,
            "CGPA": cgpa,
            "Attendance_Percentage": attendance,
            "Technical_Skills": technical_skills,
            "Internships": internships,
            "Projects": projects,
            "Certifications": certifications,
            "Aptitude_Score": aptitude_score,
            "Communication_Score": communication_score,
            "Placement_Status": placement_status,
            "Company": company,
            "Salary_Package_LPA": salary_package,
        }
    )

    return df


def main():
    print("=" * 70)
    print("STUDENT PERFORMANCE & PLACEMENT ANALYTICS - DATA GENERATOR")
    print("=" * 70)

    df = generate_dataset(NUM_STUDENTS)

    # Ensure output directory exists (relative path, Windows compatible)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "data")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "student_placement_data.csv")

    df.to_csv(output_path, index=False)

    print(f"\nGenerated {len(df)} student records.")
    print(f"Saved to: {output_path}")
    print(f"\nPlacement rate: {(df['Placement_Status'] == 'Placed').mean() * 100:.2f}%")
    print(f"Average CGPA: {df['CGPA'].mean():.2f}")
    print(f"Average Salary (placed): {df.loc[df['Placement_Status']=='Placed', 'Salary_Package_LPA'].mean():.2f} LPA")
    print("\nSample records:")
    print(df.head(5).to_string(index=False))
    print("\nData generation completed successfully.")


if __name__ == "__main__":
    main()
