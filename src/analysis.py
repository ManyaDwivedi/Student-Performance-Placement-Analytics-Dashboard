"""
analysis.py
-----------
Performs complete exploratory data analysis, statistical analysis, and
correlation analysis on the cleaned student placement dataset. Also
generates all visualizations and the final project insights report.

Run:
    python src/analysis.py
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    load_clean_data, add_cgpa_range, placement_rate,
    ensure_dir, VIS_DIR, REPORTS_DIR, CGPA_LABELS,
)

warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 120
PALETTE = "viridis"


# ---------------------------------------------------------------------------
# Core computed insights (dynamic — used by both report & dashboard logic)
# ---------------------------------------------------------------------------
def compute_insights(df):
    df = add_cgpa_range(df)
    placed_df = df[df["Placement_Status"] == "Placed"]

    insights = {}
    insights["total_students"] = len(df)
    insights["total_placed"] = len(placed_df)
    insights["total_not_placed"] = len(df) - len(placed_df)
    insights["placement_rate"] = placement_rate(df)

    insights["avg_cgpa"] = df["CGPA"].mean()
    insights["avg_attendance"] = df["Attendance_Percentage"].mean()
    insights["avg_technical_skills"] = df["Technical_Skills"].mean()
    insights["avg_internships"] = df["Internships"].mean()
    insights["avg_projects"] = df["Projects"].mean()
    insights["avg_certifications"] = df["Certifications"].mean()

    insights["avg_salary"] = placed_df["Salary_Package_LPA"].mean() if len(placed_df) else 0
    insights["highest_salary"] = placed_df["Salary_Package_LPA"].max() if len(placed_df) else 0
    insights["lowest_salary"] = placed_df["Salary_Package_LPA"].min() if len(placed_df) else 0

    # Branch level
    branch_cgpa = df.groupby("Branch")["CGPA"].mean().sort_values(ascending=False)
    insights["branch_highest_cgpa"] = branch_cgpa.index[0]
    insights["branch_highest_cgpa_value"] = branch_cgpa.iloc[0]

    branch_placement = df.groupby("Branch").apply(placement_rate).sort_values(ascending=False)
    insights["branch_highest_placement_rate"] = branch_placement.index[0]
    insights["branch_highest_placement_rate_value"] = branch_placement.iloc[0]

    branch_salary = placed_df.groupby("Branch")["Salary_Package_LPA"].mean().sort_values(ascending=False)
    if len(branch_salary):
        insights["branch_highest_salary"] = branch_salary.index[0]
        insights["branch_highest_salary_value"] = branch_salary.iloc[0]
    else:
        insights["branch_highest_salary"] = "N/A"
        insights["branch_highest_salary_value"] = 0

    # CGPA range placement
    cgpa_range_placement = df.groupby("CGPA_Range", observed=True).apply(placement_rate)
    cgpa_range_placement = cgpa_range_placement.reindex(CGPA_LABELS)
    insights["cgpa_range_placement"] = cgpa_range_placement
    insights["best_cgpa_range"] = cgpa_range_placement.idxmax()
    insights["best_cgpa_range_value"] = cgpa_range_placement.max()

    # Attendance vs placement
    insights["avg_attendance_placed"] = placed_df["Attendance_Percentage"].mean() if len(placed_df) else 0
    not_placed_df = df[df["Placement_Status"] == "Not Placed"]
    insights["avg_attendance_not_placed"] = not_placed_df["Attendance_Percentage"].mean() if len(not_placed_df) else 0

    # Company level
    company_counts = placed_df["Company"].value_counts()
    insights["top_company"] = company_counts.index[0] if len(company_counts) else "N/A"
    insights["top_company_count"] = company_counts.iloc[0] if len(company_counts) else 0

    company_salary = placed_df.groupby("Company")["Salary_Package_LPA"].mean().sort_values(ascending=False)
    insights["top_paying_company"] = company_salary.index[0] if len(company_salary) else "N/A"
    insights["top_paying_company_value"] = company_salary.iloc[0] if len(company_salary) else 0

    # Gender
    gender_placement = df.groupby("Gender").apply(placement_rate)
    insights["gender_placement"] = gender_placement

    # Experience factor impact (correlation with placement, encoded)
    df_encoded = df.copy()
    df_encoded["Placed_Binary"] = (df_encoded["Placement_Status"] == "Placed").astype(int)
    factor_cols = ["Technical_Skills", "Internships", "Projects", "Certifications",
                   "Aptitude_Score", "Communication_Score", "CGPA", "Attendance_Percentage"]
    factor_corr = df_encoded[factor_cols + ["Placed_Binary"]].corr()["Placed_Binary"].drop("Placed_Binary")
    factor_corr = factor_corr.sort_values(ascending=False)
    insights["factor_corr"] = factor_corr
    insights["most_influential_factor"] = factor_corr.idxmax()
    insights["most_influential_factor_value"] = factor_corr.max()

    # Correlation matrix (numeric features incl. salary)
    corr_cols = ["CGPA", "Attendance_Percentage", "Technical_Skills", "Internships",
                 "Projects", "Certifications", "Aptitude_Score", "Communication_Score",
                 "Salary_Package_LPA"]
    corr_matrix = df[corr_cols].corr()
    insights["corr_matrix"] = corr_matrix
    salary_corr = corr_matrix["Salary_Package_LPA"].drop("Salary_Package_LPA").sort_values(ascending=False)
    insights["strongest_salary_corr_feature"] = salary_corr.idxmax()
    insights["strongest_salary_corr_value"] = salary_corr.max()

    return insights


# ---------------------------------------------------------------------------
# Visualization generation
# ---------------------------------------------------------------------------
def savefig(name):
    path = os.path.join(VIS_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {name}")


def generate_visualizations(df):
    ensure_dir(VIS_DIR)
    df = add_cgpa_range(df)
    placed_df = df[df["Placement_Status"] == "Placed"]

    print("\nGenerating visualizations...")

    # 1. Placement Status Distribution
    plt.figure(figsize=(7, 6))
    counts = df["Placement_Status"].value_counts()
    colors = ["#2E86AB", "#E76F51"]
    plt.pie(counts, labels=counts.index, autopct="%1.1f%%", colors=colors,
            startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    plt.title("Placement Status Distribution", fontsize=14, fontweight="bold")
    savefig("placement_distribution.png")

    # 2. Branch-wise Placement Rate
    plt.figure(figsize=(10, 6))
    branch_rate = df.groupby("Branch").apply(placement_rate).sort_values(ascending=False)
    sns.barplot(x=branch_rate.values, y=branch_rate.index, hue=branch_rate.index,
                palette=PALETTE, legend=False)
    plt.xlabel("Placement Rate (%)")
    plt.ylabel("Branch")
    plt.title("Branch-wise Placement Rate", fontsize=14, fontweight="bold")
    plt.grid(axis="x", alpha=0.3)
    savefig("branch_placement_rate.png")

    # 3. CGPA Distribution
    plt.figure(figsize=(9, 6))
    sns.histplot(df["CGPA"], bins=25, kde=True, color="#2E86AB")
    plt.xlabel("CGPA")
    plt.ylabel("Number of Students")
    plt.title("CGPA Distribution", fontsize=14, fontweight="bold")
    savefig("cgpa_distribution.png")

    # 4. Average CGPA by Branch
    plt.figure(figsize=(10, 6))
    avg_cgpa_branch = df.groupby("Branch")["CGPA"].mean().sort_values(ascending=False)
    sns.barplot(x=avg_cgpa_branch.values, y=avg_cgpa_branch.index,
                hue=avg_cgpa_branch.index, palette="crest", legend=False)
    plt.xlabel("Average CGPA")
    plt.ylabel("Branch")
    plt.title("Average CGPA by Branch", fontsize=14, fontweight="bold")
    plt.grid(axis="x", alpha=0.3)
    savefig("average_cgpa_by_branch.png")

    # 5. CGPA vs Salary Package
    plt.figure(figsize=(9, 6))
    sns.scatterplot(data=placed_df, x="CGPA", y="Salary_Package_LPA",
                     hue="Branch", palette="tab10", alpha=0.7, s=45)
    plt.xlabel("CGPA")
    plt.ylabel("Salary Package (LPA)")
    plt.title("CGPA vs Salary Package (Placed Students)", fontsize=14, fontweight="bold")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    savefig("cgpa_vs_salary.png")

    # 6. Attendance vs Placement
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x="Placement_Status", y="Attendance_Percentage",
                hue="Placement_Status", palette=["#E76F51", "#2E86AB"], legend=False)
    plt.xlabel("Placement Status")
    plt.ylabel("Attendance Percentage")
    plt.title("Attendance vs Placement Status", fontsize=14, fontweight="bold")
    savefig("attendance_vs_placement.png")

    # 7. Internships vs Placement
    plt.figure(figsize=(9, 6))
    intern_rate = df.groupby("Internships").apply(placement_rate)
    sns.barplot(x=intern_rate.index, y=intern_rate.values, hue=intern_rate.index,
                palette=PALETTE, legend=False)
    plt.xlabel("Number of Internships")
    plt.ylabel("Placement Rate (%)")
    plt.title("Internships vs Placement Rate", fontsize=14, fontweight="bold")
    plt.grid(axis="y", alpha=0.3)
    savefig("internships_vs_placement.png")

    # 8. Projects vs Placement
    plt.figure(figsize=(9, 6))
    proj_rate = df.groupby("Projects").apply(placement_rate)
    sns.barplot(x=proj_rate.index, y=proj_rate.values, hue=proj_rate.index,
                palette=PALETTE, legend=False)
    plt.xlabel("Number of Projects")
    plt.ylabel("Placement Rate (%)")
    plt.title("Projects vs Placement Rate", fontsize=14, fontweight="bold")
    plt.grid(axis="y", alpha=0.3)
    savefig("projects_vs_placement.png")

    # 9. Certifications vs Placement
    plt.figure(figsize=(9, 6))
    cert_rate = df.groupby("Certifications").apply(placement_rate)
    sns.barplot(x=cert_rate.index, y=cert_rate.values, hue=cert_rate.index,
                palette=PALETTE, legend=False)
    plt.xlabel("Number of Certifications")
    plt.ylabel("Placement Rate (%)")
    plt.title("Certifications vs Placement Rate", fontsize=14, fontweight="bold")
    plt.grid(axis="y", alpha=0.3)
    savefig("certifications_vs_placement.png")

    # 10. Gender-wise Placement
    plt.figure(figsize=(8, 6))
    gender_ct = pd.crosstab(df["Gender"], df["Placement_Status"])
    gender_ct.plot(kind="bar", stacked=True, color=["#E76F51", "#2E86AB"], ax=plt.gca())
    plt.xlabel("Gender")
    plt.ylabel("Number of Students")
    plt.title("Gender-wise Placement", fontsize=14, fontweight="bold")
    plt.xticks(rotation=0)
    plt.legend(title="Placement Status")
    savefig("gender_wise_placement.png")

    # 11. Company-wise Placement
    plt.figure(figsize=(10, 6))
    company_counts = placed_df["Company"].value_counts()
    sns.barplot(x=company_counts.values, y=company_counts.index,
                hue=company_counts.index, palette="mako", legend=False)
    plt.xlabel("Number of Students Placed")
    plt.ylabel("Company")
    plt.title("Company-wise Placement Count", fontsize=14, fontweight="bold")
    plt.grid(axis="x", alpha=0.3)
    savefig("company_wise_placement.png")

    # 12. Salary Distribution
    plt.figure(figsize=(9, 6))
    sns.histplot(placed_df["Salary_Package_LPA"], bins=25, kde=True, color="#2A9D8F")
    plt.xlabel("Salary Package (LPA)")
    plt.ylabel("Number of Students")
    plt.title("Salary Distribution (Placed Students)", fontsize=14, fontweight="bold")
    savefig("salary_distribution.png")

    # 13. Branch-wise Average Salary
    plt.figure(figsize=(10, 6))
    branch_salary = placed_df.groupby("Branch")["Salary_Package_LPA"].mean().sort_values(ascending=False)
    sns.barplot(x=branch_salary.values, y=branch_salary.index,
                hue=branch_salary.index, palette="crest", legend=False)
    plt.xlabel("Average Salary Package (LPA)")
    plt.ylabel("Branch")
    plt.title("Branch-wise Average Salary", fontsize=14, fontweight="bold")
    plt.grid(axis="x", alpha=0.3)
    savefig("branch_wise_average_salary.png")

    # 14. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    corr_cols = ["CGPA", "Attendance_Percentage", "Technical_Skills", "Internships",
                 "Projects", "Certifications", "Aptitude_Score", "Communication_Score",
                 "Salary_Package_LPA"]
    corr = df[corr_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title("Correlation Heatmap of Numeric Features", fontsize=14, fontweight="bold")
    savefig("correlation_heatmap.png")

    print("All 14 visualizations generated successfully.")


# ---------------------------------------------------------------------------
# Insights report
# ---------------------------------------------------------------------------
def generate_report(insights):
    ensure_dir(REPORTS_DIR)
    report_path = os.path.join(REPORTS_DIR, "project_insights.md")

    cgpa_range_lines = "\n".join(
        f"- **{rng}**: {val:.2f}% placement rate"
        for rng, val in insights["cgpa_range_placement"].items()
    )

    factor_lines = "\n".join(
        f"- **{factor}**: correlation = {val:.3f}"
        for factor, val in insights["factor_corr"].items()
    )

    gender_lines = "\n".join(
        f"- **{g}**: {val:.2f}% placement rate"
        for g, val in insights["gender_placement"].items()
    )

    content = f"""# Project Insights — Student Performance & Placement Analytics

*All figures below are calculated directly from the generated dataset
(`data/cleaned_student_data.csv`).*

## Overall Insights

- **Total Students:** {insights['total_students']}
- **Placed Students:** {insights['total_placed']}
- **Not Placed Students:** {insights['total_not_placed']}
- **Placement Rate:** {insights['placement_rate']:.2f}%
- **Average CGPA:** {insights['avg_cgpa']:.2f}
- **Average Salary Package:** {insights['avg_salary']:.2f} LPA
- **Highest Salary Package:** {insights['highest_salary']:.2f} LPA
- **Lowest Salary Package (placed):** {insights['lowest_salary']:.2f} LPA

## Academic Insights

- **Branch with highest average CGPA:** {insights['branch_highest_cgpa']} ({insights['branch_highest_cgpa_value']:.2f})
- **CGPA range with highest placement rate:** {insights['best_cgpa_range']} ({insights['best_cgpa_range_value']:.2f}%)

**Placement rate by CGPA range:**
{cgpa_range_lines}

- **Average attendance of placed students:** {insights['avg_attendance_placed']:.2f}%
- **Average attendance of not-placed students:** {insights['avg_attendance_not_placed']:.2f}%

Higher CGPA is generally associated with a higher chance of placement,
though the relationship is not perfectly linear — some students with
strong CGPA remain unplaced, while some with moderate CGPA but strong
internships/skills profiles do get placed. This reflects the realistic
noise deliberately built into the dataset.

## Skills Insights

**Correlation of each factor with placement outcome (higher = stronger positive impact):**
{factor_lines}

- **Most influential factor for placement:** {insights['most_influential_factor']} (correlation = {insights['most_influential_factor_value']:.3f})

Technical skills, internships, projects and certifications all show a
positive relationship with placement likelihood — students investing in
practical, hands-on experience alongside academics tend to have better
placement outcomes.

## Placement Insights

- **Branch with highest placement rate:** {insights['branch_highest_placement_rate']} ({insights['branch_highest_placement_rate_value']:.2f}%)
- **Top recruiting company:** {insights['top_company']} ({insights['top_company_count']} students placed)

**Gender-wise placement rate:**
{gender_lines}

## Salary Insights

- **Branch with highest average package:** {insights['branch_highest_salary']} ({insights['branch_highest_salary_value']:.2f} LPA)
- **Company with highest average package:** {insights['top_paying_company']} ({insights['top_paying_company_value']:.2f} LPA)
- **Feature most strongly correlated with salary:** {insights['strongest_salary_corr_feature']} (correlation = {insights['strongest_salary_corr_value']:.3f})

CGPA shows a clear positive relationship with salary package, and this
is reinforced by internships, projects and technical skills — students
who combine strong academics with hands-on experience tend to command
higher packages.

## Final Conclusion

The analysis of {insights['total_students']} student records shows an
overall placement rate of {insights['placement_rate']:.2f}%, with
**{insights['branch_highest_placement_rate']}** leading in placement
outcomes and **{insights['branch_highest_salary']}** leading in average
salary package. Academic performance (CGPA) and hands-on experience
(internships, projects, certifications, technical skills) together are
the strongest drivers of both placement likelihood and salary package.
Students aiming to improve their employability should focus on
maintaining a strong CGPA while actively building practical experience
through internships, projects and relevant certifications, alongside
developing aptitude and communication skills, which also contribute
meaningfully to placement success.

---
*Report generated automatically from the analysis pipeline — no values
in this report are hardcoded.*
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nInsights report saved to: {report_path}")


# ---------------------------------------------------------------------------
# Console EDA printout
# ---------------------------------------------------------------------------
def print_eda(insights):
    print("=" * 70)
    print("STUDENT PERFORMANCE & PLACEMENT ANALYTICS - EXPLORATORY ANALYSIS")
    print("=" * 70)

    print("\n--- OVERALL ANALYSIS ---")
    print(f"Total Students: {insights['total_students']}")
    print(f"Total Placed: {insights['total_placed']}")
    print(f"Total Not Placed: {insights['total_not_placed']}")
    print(f"Placement Rate: {insights['placement_rate']:.2f}%")
    print(f"Average CGPA: {insights['avg_cgpa']:.2f}")
    print(f"Average Attendance: {insights['avg_attendance']:.2f}%")
    print(f"Average Technical Skills: {insights['avg_technical_skills']:.2f}")
    print(f"Average Internships: {insights['avg_internships']:.2f}")
    print(f"Average Projects: {insights['avg_projects']:.2f}")
    print(f"Average Certifications: {insights['avg_certifications']:.2f}")
    print(f"Average Salary Package: {insights['avg_salary']:.2f} LPA")
    print(f"Highest Salary Package: {insights['highest_salary']:.2f} LPA")
    print(f"Lowest Salary Package (placed): {insights['lowest_salary']:.2f} LPA")

    print("\n--- ACADEMIC PERFORMANCE ---")
    print(f"Branch with highest average CGPA: {insights['branch_highest_cgpa']} "
          f"({insights['branch_highest_cgpa_value']:.2f})")
    print("Placement rate by CGPA range:")
    print(insights["cgpa_range_placement"])

    print("\n--- PLACEMENT ANALYSIS ---")
    print(f"Branch with highest placement rate: {insights['branch_highest_placement_rate']} "
          f"({insights['branch_highest_placement_rate_value']:.2f}%)")
    print(f"Top recruiting company: {insights['top_company']} "
          f"({insights['top_company_count']} students)")

    print("\n--- SALARY ANALYSIS ---")
    print(f"Branch with highest average salary: {insights['branch_highest_salary']} "
          f"({insights['branch_highest_salary_value']:.2f} LPA)")
    print(f"Company with highest average salary: {insights['top_paying_company']} "
          f"({insights['top_paying_company_value']:.2f} LPA)")

    print("\n--- CORRELATION ANALYSIS ---")
    print(f"Strongest feature correlated with salary: {insights['strongest_salary_corr_feature']} "
          f"({insights['strongest_salary_corr_value']:.3f})")
    print(f"Most influential factor for placement: {insights['most_influential_factor']} "
          f"({insights['most_influential_factor_value']:.3f})")


def main():
    df = load_clean_data()
    insights = compute_insights(df)
    print_eda(insights)
    generate_visualizations(df)
    generate_report(insights)
    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()
