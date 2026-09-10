# 🎓 Student Performance & Placement Analytics

**Transforming Student Data into Meaningful Academic and Placement Insights**

An end-to-end data analytics project that analyzes student academic
performance and placement outcomes — covering data generation, cleaning,
exploratory data analysis, visualization, and an interactive Streamlit
dashboard.

---

## Project Overview

This project simulates a realistic student placement dataset and builds
a complete analytics pipeline around it — from raw data generation to a
polished, interactive dashboard. It explores how academic performance
(CGPA, attendance) and hands-on experience (internships, projects,
certifications, technical skills, aptitude, and communication scores)
relate to placement outcomes and salary packages.

## Problem Statement

Educational institutions and students alike want to understand what
actually drives successful campus placements. Is CGPA the only thing
that matters? Do internships and projects matter more than certifications?
Does attendance affect outcomes? This project answers these questions
using a data-driven approach — surfacing patterns that can guide
students on where to focus their effort and help institutions understand
placement trends across branches.

## Objectives

- Generate a realistic, statistically sound synthetic dataset of student
  academic and placement records.
- Clean and validate the dataset for consistency and correctness.
- Perform thorough exploratory and statistical analysis.
- Visualize key relationships between academic/skill factors and
  placement outcomes.
- Build an interactive dashboard for exploring the data dynamically.
- Summarize findings into a clear, data-driven insights report.

## Features

- 800-record realistic synthetic dataset with logical placement and
  salary relationships.
- Full data cleaning and validation pipeline (duplicates, missing
  values, range validation, placement-logic consistency).
- Complete exploratory data analysis: overall, academic, skills,
  placement, salary, and correlation analysis.
- 14 professional, high-resolution visualizations (Matplotlib/Seaborn).
- Automatically generated insights report — no hardcoded values.
- 7-page interactive Streamlit dashboard with dynamic filters
  (Branch / Gender / Placement Status), KPI cards, and Plotly charts.
- Dataset explorer with summary statistics and CSV download.
- Basic automated test suite validating data integrity.
- Windows-friendly one-click run script.

## Technology Stack

| Category            | Tools / Libraries        |
|---------------------|---------------------------|
| Language             | Python 3.12+              |
| Data Analysis        | Pandas, NumPy             |
| Static Visualization  | Matplotlib, Seaborn       |
| Interactive Visualization | Plotly                |
| Dashboard            | Streamlit                 |
| Testing              | unittest                  |

## Dataset

The dataset (`data/student_placement_data.csv`, 800 records) contains:

| Column | Description |
|---|---|
| Student_ID | Unique student identifier (e.g. STU001) |
| Student_Name | Fictional student name |
| Gender | Male / Female / Other |
| Age | Student age (20–25) |
| Branch | Engineering branch |
| CGPA | Cumulative GPA (5.0–10.0) |
| Attendance_Percentage | Attendance (50–100%) |
| Technical_Skills | Number of technical skills (1–10) |
| Internships | Number of internships completed (0–4) |
| Projects | Number of projects completed (0–8) |
| Certifications | Number of certifications (0–10) |
| Aptitude_Score | Aptitude test score (0–100) |
| Communication_Score | Communication skill score (0–100) |
| Placement_Status | Placed / Not Placed |
| Company | Recruiting company (or "Not Applicable") |
| Salary_Package_LPA | Salary package in LPA (0 if not placed) |

Placement and salary are generated using a weighted, logistic-style
model based on CGPA, attendance, skills, internships, projects,
certifications, aptitude, and communication — with realistic random
noise so outcomes aren't perfectly predictable.

## Data Analytics Workflow

```
Raw Data
   ↓
Data Cleaning
   ↓
Data Validation
   ↓
Exploratory Data Analysis
   ↓
Visualization
   ↓
Interactive Dashboard
   ↓
Business Insights
```

## Project Structure

```
Student-Performance-Placement-Analytics/
├── data/
│   ├── student_placement_data.csv
│   └── cleaned_student_data.csv
├── src/
│   ├── __init__.py
│   ├── data_generator.py
│   ├── data_cleaning.py
│   ├── analysis.py
│   └── utils.py
├── dashboard/
│   └── app.py
├── visualizations/
│   ├── placement_distribution.png
│   ├── branch_placement_rate.png
│   ├── cgpa_distribution.png
│   ├── average_cgpa_by_branch.png
│   ├── cgpa_vs_salary.png
│   ├── attendance_vs_placement.png
│   ├── internships_vs_placement.png
│   ├── projects_vs_placement.png
│   ├── certifications_vs_placement.png
│   ├── gender_wise_placement.png
│   ├── company_wise_placement.png
│   ├── salary_distribution.png
│   ├── branch_wise_average_salary.png
│   └── correlation_heatmap.png
├── reports/
│   └── project_insights.md
├── tests/
│   └── test_project.py
├── .gitignore
├── requirements.txt
├── README.md
└── run_project.bat
```

## Installation

```
git clone YOUR_REPOSITORY_URL
cd Student-Performance-Placement-Analytics
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> On Windows, you can instead simply double-click `run_project.bat`,
> which automates all of the steps below.

## Run Dataset Generator

```
python src/data_generator.py
```

## Run Data Cleaning

```
python src/data_cleaning.py
```

## Run Analysis

```
python src/analysis.py
```

This generates all 14 visualizations in `visualizations/` and the
insights report at `reports/project_insights.md`.

## Run Dashboard

```
streamlit run dashboard/app.py
```

## Dashboard Features

The dashboard opens with a sidebar for navigation and dynamic filters
(Branch, Gender, Placement Status — each with an "All" option):

1. **Overview** — KPI cards (total students, placed, placement rate,
   average CGPA, average/highest salary) plus placement, branch, and
   gender distribution charts.
2. **Academic Performance** — CGPA distribution, average CGPA by
   branch, CGPA/attendance vs placement, and CGPA-range placement
   analysis.
3. **Skills & Experience** — Technical skills, internships, projects,
   certifications, aptitude, and communication vs placement.
4. **Placement Analysis** — Overall distribution, branch/gender/company
   breakdowns, and top recruiting companies.
5. **Salary Analysis** — Salary distribution, branch/company-wise
   average salary, and salary vs CGPA/internships/projects.
6. **Key Insights** — Dynamically calculated highlight cards (top
   branch, top company, best CGPA range, most influential factor,
   strongest salary correlation, etc.) — nothing is hardcoded.
7. **Dataset Explorer** — Data preview, shape, dtypes, missing-value
   summary, full summary statistics, and a CSV download button for the
   currently filtered data.

## Key Insights

*(Calculated automatically — see `reports/project_insights.md` for the
full, always-up-to-date report.)*

- **Total Students:** 800 | **Placement Rate:** 44.00%
- **Average CGPA:** 7.45 | **Average Salary Package:** 10.25 LPA
- **Highest Salary Package:** 16.73 LPA
- **Branch with highest placement rate:** Computer Science Engineering (47.27%)
- **Branch with highest average salary:** Mechanical Engineering (10.64 LPA)
- **CGPA range with best placement rate:** Above 9 (65.96%)
- **Most influential factor for placement:** CGPA (correlation = 0.124)
- **Top recruiting company:** Capgemini (44 students placed)
- **Feature most strongly correlated with salary:** CGPA (correlation = 0.199)

## Visualizations

All 14 charts are saved in `visualizations/` after running
`python src/analysis.py`, including placement distribution, branch-wise
placement rate, CGPA distribution, CGPA vs salary, attendance/
internships/projects/certifications vs placement, gender- and
company-wise placement, salary distribution, branch-wise average
salary, and a full correlation heatmap.

## Future Improvements

- Machine Learning-based placement prediction model
- Salary prediction model
- Student career recommendation engine
- Real-time database integration
- Advanced statistical analysis (hypothesis testing, ANOVA)
- More dashboard filters (CGPA range, internship count, etc.)

## Author

**Manya Dwivedi**
Computer Science Engineering — Artificial Intelligence & Machine Learning
