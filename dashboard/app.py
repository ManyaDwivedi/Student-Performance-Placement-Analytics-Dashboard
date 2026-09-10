"""
app.py
------
Student Performance & Placement Analytics Dashboard.
A modern, interactive Streamlit dashboard built entirely from the
cleaned dataset. Run with:

    streamlit run dashboard/app.py
"""

import os
import sys

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from utils import CLEAN_DATA_PATH, add_cgpa_range, placement_rate, CGPA_LABELS  # noqa: E402

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Performance & Placement Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY = "#2E86AB"
ACCENT = "#E76F51"
SUCCESS = "#2A9D8F"
NEUTRAL_BG = "#F5F7FA"

CUSTOM_CSS = f"""
<style>
    .main {{
        background-color: {NEUTRAL_BG};
    }}
    .kpi-card {{
        background: white;
        border-radius: 12px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border-left: 5px solid {PRIMARY};
        margin-bottom: 0.6rem;
    }}
    .kpi-label {{
        font-size: 0.82rem;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }}
    .kpi-value {{
        font-size: 1.7rem;
        font-weight: 700;
        color: #1f2937;
    }}
    .insight-card {{
        background: white;
        border-radius: 12px;
        padding: 1rem 1.3rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border-left: 5px solid {SUCCESS};
        margin-bottom: 0.9rem;
    }}
    .insight-title {{
        font-weight: 700;
        color: {SUCCESS};
        font-size: 0.95rem;
        margin-bottom: 0.2rem;
    }}
    .insight-value {{
        font-size: 1.15rem;
        color: #1f2937;
        font-weight: 600;
    }}
    h1, h2, h3 {{
        color: #1f2937;
    }}
    .section-header {{
        border-bottom: 2px solid {PRIMARY};
        padding-bottom: 0.3rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #dff6ff 0%, #bfeaff 100%);
        color: #18384f;
    }}
    [data-testid="stSidebar"] * {{
        color: #18384f;
    }}
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .st-bb,
    [data-testid="stSidebar"] .stRadio,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stTextInput,
    [data-testid="stSidebar"] .stCheckbox {{
        color: #18384f;
    }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Data loading (with caching and error handling)
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    if not os.path.exists(CLEAN_DATA_PATH):
        return None
    try:
        df = pd.read_csv(CLEAN_DATA_PATH)
    except Exception:
        return None
    if df.empty:
        return None
    required_cols = [
        "Student_ID", "Gender", "Age", "Branch", "CGPA",
        "Attendance_Percentage", "Technical_Skills", "Internships",
        "Projects", "Certifications", "Aptitude_Score",
        "Communication_Score", "Placement_Status", "Company",
        "Salary_Package_LPA",
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        return None
    df = add_cgpa_range(df)
    return df


df_full = load_data()

if df_full is None:
    st.error(
        "**Dataset could not be loaded.**\n\n"
        "Please make sure you have run the following commands first:\n\n"
        "```\npython src/data_generator.py\npython src/data_cleaning.py\n```\n\n"
        f"Expected cleaned dataset at: `{CLEAN_DATA_PATH}`"
    )
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar — navigation & filters
# ---------------------------------------------------------------------------
st.sidebar.title("🎓 Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Academic Performance",
        "Skills & Experience",
        "Placement Analysis",
        "Salary Analysis",
        "Key Insights",
        "Dataset Explorer",
    ],
)

st.sidebar.markdown("---")
st.sidebar.title("🔍 Filters")

branch_options = ["All"] + sorted(df_full["Branch"].unique().tolist())
gender_options = ["All"] + sorted(df_full["Gender"].unique().tolist())
placement_options = ["All"] + sorted(df_full["Placement_Status"].unique().tolist())

sel_branch = st.sidebar.selectbox("Branch", branch_options, index=0)
sel_gender = st.sidebar.selectbox("Gender", gender_options, index=0)
sel_placement = st.sidebar.selectbox("Placement Status", placement_options, index=0)

df = df_full.copy()
if sel_branch != "All":
    df = df[df["Branch"] == sel_branch]
if sel_gender != "All":
    df = df[df["Gender"] == sel_gender]
if sel_placement != "All":
    df = df[df["Placement_Status"] == sel_placement]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(df)}** of **{len(df_full)}** student records.")

if df.empty:
    st.warning("No records match the selected filters. Please adjust your filters.")
    st.stop()

placed_df = df[df["Placement_Status"] == "Placed"]


def kpi_card(label, value):
    st.markdown(
        f"""<div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>""",
        unsafe_allow_html=True,
    )


def insight_card(title, value):
    st.markdown(
        f"""<div class="insight-card">
                <div class="insight-title">{title}</div>
                <div class="insight-value">{value}</div>
            </div>""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🎓 Student Performance & Placement Analytics Dashboard")
st.caption("Transforming Student Data into Meaningful Academic and Placement Insights")
st.markdown("---")


# ===========================================================================
# PAGE 1 — OVERVIEW
# ===========================================================================
if page == "Overview":
    st.subheader("📊 Overview")

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Total Students", f"{len(df):,}")
    with c2:
        kpi_card("Placed Students", f"{len(placed_df):,}")
    with c3:
        kpi_card("Placement Rate", f"{placement_rate(df):.2f}%")

    c4, c5, c6 = st.columns(3)
    with c4:
        kpi_card("Average CGPA", f"{df['CGPA'].mean():.2f}")
    with c5:
        avg_sal = placed_df["Salary_Package_LPA"].mean() if len(placed_df) else 0
        kpi_card("Average Salary Package", f"{avg_sal:.2f} LPA")
    with c6:
        max_sal = placed_df["Salary_Package_LPA"].max() if len(placed_df) else 0
        kpi_card("Highest Salary Package", f"{max_sal:.2f} LPA")

    st.markdown("<div class='section-header'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Placement Distribution**")
        counts = df["Placement_Status"].value_counts().reset_index()
        counts.columns = ["Placement_Status", "Count"]
        fig = px.pie(counts, names="Placement_Status", values="Count",
                     color="Placement_Status",
                     color_discrete_map={"Placed": PRIMARY, "Not Placed": ACCENT},
                     hole=0.45)
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Branch-wise Placement Rate**")
        branch_rate = df.groupby("Branch").apply(placement_rate).sort_values(ascending=False).reset_index()
        branch_rate.columns = ["Branch", "Placement Rate (%)"]
        fig = px.bar(branch_rate, x="Placement Rate (%)", y="Branch", orientation="h",
                     color="Placement Rate (%)", color_continuous_scale="Viridis")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Gender-wise Placement Rate**")
    gender_ct = pd.crosstab(df["Gender"], df["Placement_Status"]).reset_index()
    fig = px.bar(gender_ct, x="Gender", y=[c for c in gender_ct.columns if c != "Gender"],
                 barmode="group", color_discrete_sequence=[ACCENT, PRIMARY])
    fig.update_layout(yaxis_title="Number of Students", legend_title="Placement Status")
    st.plotly_chart(fig, use_container_width=True)


# ===========================================================================
# PAGE 2 — ACADEMIC PERFORMANCE
# ===========================================================================
elif page == "Academic Performance":
    st.subheader("📚 Academic Performance")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**CGPA Distribution**")
        fig = px.histogram(df, x="CGPA", nbins=25, color_discrete_sequence=[PRIMARY])
        fig.update_layout(yaxis_title="Number of Students")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Average CGPA by Branch**")
        avg_cgpa = df.groupby("Branch")["CGPA"].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(avg_cgpa, x="CGPA", y="Branch", orientation="h",
                     color="CGPA", color_continuous_scale="Teal")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**CGPA vs Placement Status**")
        fig = px.box(df, x="Placement_Status", y="CGPA", color="Placement_Status",
                     color_discrete_map={"Placed": PRIMARY, "Not Placed": ACCENT})
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("**Attendance vs Placement Status**")
        fig = px.box(df, x="Placement_Status", y="Attendance_Percentage", color="Placement_Status",
                     color_discrete_map={"Placed": PRIMARY, "Not Placed": ACCENT})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**CGPA Range vs Placement Rate**")
    cgpa_range_rate = df.groupby("CGPA_Range", observed=True).apply(placement_rate)
    cgpa_range_rate = cgpa_range_rate.reindex(CGPA_LABELS).reset_index()
    cgpa_range_rate.columns = ["CGPA Range", "Placement Rate (%)"]
    fig = px.bar(cgpa_range_rate, x="CGPA Range", y="Placement Rate (%)",
                 color="Placement Rate (%)", color_continuous_scale="Viridis", text_auto=".1f")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Higher CGPA ranges generally show higher placement rates, though the "
               "trend includes realistic variation rather than a perfectly linear pattern.")


# ===========================================================================
# PAGE 3 — SKILLS & EXPERIENCE
# ===========================================================================
elif page == "Skills & Experience":
    st.subheader("🛠️ Skills & Experience")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Technical Skills vs Placement Rate**")
        rate = df.groupby("Technical_Skills").apply(placement_rate).reset_index()
        rate.columns = ["Technical_Skills", "Placement Rate (%)"]
        fig = px.bar(rate, x="Technical_Skills", y="Placement Rate (%)",
                     color="Placement Rate (%)", color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Internships vs Placement Rate**")
        rate = df.groupby("Internships").apply(placement_rate).reset_index()
        rate.columns = ["Internships", "Placement Rate (%)"]
        fig = px.bar(rate, x="Internships", y="Placement Rate (%)",
                     color="Placement Rate (%)", color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Projects vs Placement Rate**")
        rate = df.groupby("Projects").apply(placement_rate).reset_index()
        rate.columns = ["Projects", "Placement Rate (%)"]
        fig = px.bar(rate, x="Projects", y="Placement Rate (%)",
                     color="Placement Rate (%)", color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("**Certifications vs Placement Rate**")
        rate = df.groupby("Certifications").apply(placement_rate).reset_index()
        rate.columns = ["Certifications", "Placement Rate (%)"]
        fig = px.bar(rate, x="Certifications", y="Placement Rate (%)",
                     color="Placement Rate (%)", color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("**Aptitude Score vs Placement**")
        fig = px.box(df, x="Placement_Status", y="Aptitude_Score", color="Placement_Status",
                     color_discrete_map={"Placed": PRIMARY, "Not Placed": ACCENT})
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        st.markdown("**Communication Score vs Placement**")
        fig = px.box(df, x="Placement_Status", y="Communication_Score", color="Placement_Status",
                     color_discrete_map={"Placed": PRIMARY, "Not Placed": ACCENT})
        st.plotly_chart(fig, use_container_width=True)


# ===========================================================================
# PAGE 4 — PLACEMENT ANALYSIS
# ===========================================================================
elif page == "Placement Analysis":
    st.subheader("🎯 Placement Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Overall Placement Distribution**")
        counts = df["Placement_Status"].value_counts().reset_index()
        counts.columns = ["Placement_Status", "Count"]
        fig = px.pie(counts, names="Placement_Status", values="Count",
                     color="Placement_Status",
                     color_discrete_map={"Placed": PRIMARY, "Not Placed": ACCENT}, hole=0.45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Branch-wise Placement Rate**")
        branch_rate = df.groupby("Branch").apply(placement_rate).sort_values(ascending=False).reset_index()
        branch_rate.columns = ["Branch", "Placement Rate (%)"]
        fig = px.bar(branch_rate, x="Placement Rate (%)", y="Branch", orientation="h",
                     color="Placement Rate (%)", color_continuous_scale="Viridis")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Gender-wise Placement**")
        gender_ct = pd.crosstab(df["Gender"], df["Placement_Status"]).reset_index()
        fig = px.bar(gender_ct, x="Gender", y=[c for c in gender_ct.columns if c != "Gender"],
                     barmode="group", color_discrete_sequence=[ACCENT, PRIMARY])
        fig.update_layout(yaxis_title="Number of Students", legend_title="Placement Status")
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("**Company-wise Placement**")
        company_counts = placed_df["Company"].value_counts().reset_index()
        company_counts.columns = ["Company", "Count"]
        if not company_counts.empty:
            fig = px.bar(company_counts, x="Count", y="Company", orientation="h",
                         color="Count", color_continuous_scale="Mako" if False else "Viridis")
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No placed students in current filter selection.")

    st.markdown("**Top Recruiting Companies**")
    if not placed_df.empty:
        top_companies = placed_df["Company"].value_counts().head(5).reset_index()
        top_companies.columns = ["Company", "Students Placed"]
        st.dataframe(top_companies, use_container_width=True, hide_index=True)
    else:
        st.info("No placed students in current filter selection.")


# ===========================================================================
# PAGE 5 — SALARY ANALYSIS
# ===========================================================================
elif page == "Salary Analysis":
    st.subheader("💰 Salary Analysis")

    if placed_df.empty:
        st.info("No placed students in the current filter selection to analyze salary.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Salary Distribution**")
            fig = px.histogram(placed_df, x="Salary_Package_LPA", nbins=25,
                                color_discrete_sequence=[SUCCESS])
            fig.update_layout(yaxis_title="Number of Students")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Branch-wise Average Salary**")
            branch_sal = placed_df.groupby("Branch")["Salary_Package_LPA"].mean().sort_values(ascending=False).reset_index()
            fig = px.bar(branch_sal, x="Salary_Package_LPA", y="Branch", orientation="h",
                         color="Salary_Package_LPA", color_continuous_scale="Teal")
            fig.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Average Salary (LPA)")
            st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown("**Company-wise Average Salary**")
            company_sal = placed_df.groupby("Company")["Salary_Package_LPA"].mean().sort_values(ascending=False).reset_index()
            fig = px.bar(company_sal, x="Salary_Package_LPA", y="Company", orientation="h",
                         color="Salary_Package_LPA", color_continuous_scale="Viridis")
            fig.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Average Salary (LPA)")
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            st.markdown("**CGPA vs Salary**")
            fig = px.scatter(placed_df, x="CGPA", y="Salary_Package_LPA", color="Branch",
                              opacity=0.7)
            st.plotly_chart(fig, use_container_width=True)

        col5, col6 = st.columns(2)
        with col5:
            st.markdown("**Internships vs Salary**")
            rate = placed_df.groupby("Internships")["Salary_Package_LPA"].mean().reset_index()
            fig = px.bar(rate, x="Internships", y="Salary_Package_LPA",
                         color="Salary_Package_LPA", color_continuous_scale="Viridis")
            fig.update_layout(yaxis_title="Average Salary (LPA)")
            st.plotly_chart(fig, use_container_width=True)

        with col6:
            st.markdown("**Projects vs Salary**")
            rate = placed_df.groupby("Projects")["Salary_Package_LPA"].mean().reset_index()
            fig = px.bar(rate, x="Projects", y="Salary_Package_LPA",
                         color="Salary_Package_LPA", color_continuous_scale="Viridis")
            fig.update_layout(yaxis_title="Average Salary (LPA)")
            st.plotly_chart(fig, use_container_width=True)


# ===========================================================================
# PAGE 6 — KEY INSIGHTS
# ===========================================================================
elif page == "Key Insights":
    st.subheader("💡 Key Insights")
    st.caption("All values below are calculated dynamically from the currently filtered dataset.")

    branch_rate = df.groupby("Branch").apply(placement_rate).sort_values(ascending=False)
    branch_salary = placed_df.groupby("Branch")["Salary_Package_LPA"].mean().sort_values(ascending=False) if not placed_df.empty else pd.Series(dtype=float)
    cgpa_range_rate = df.groupby("CGPA_Range", observed=True).apply(placement_rate).reindex(CGPA_LABELS)

    df_encoded = df.copy()
    df_encoded["Placed_Binary"] = (df_encoded["Placement_Status"] == "Placed").astype(int)
    factor_cols = ["Technical_Skills", "Internships", "Projects", "Certifications",
                   "Aptitude_Score", "Communication_Score"]
    factor_corr = df_encoded[factor_cols + ["Placed_Binary"]].corr()["Placed_Binary"].drop("Placed_Binary").sort_values(ascending=False)

    company_counts = placed_df["Company"].value_counts() if not placed_df.empty else pd.Series(dtype=int)

    corr_cols = ["CGPA", "Attendance_Percentage", "Technical_Skills", "Internships",
                 "Projects", "Certifications", "Aptitude_Score", "Communication_Score",
                 "Salary_Package_LPA"]
    corr_matrix = df[corr_cols].corr()
    salary_corr = corr_matrix["Salary_Package_LPA"].drop("Salary_Package_LPA").sort_values(ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        if len(branch_rate):
            insight_card("🏆 Branch with Highest Placement Rate",
                         f"{branch_rate.index[0]} — {branch_rate.iloc[0]:.2f}%")
        if len(branch_salary):
            insight_card("💰 Branch with Highest Average Salary",
                         f"{branch_salary.index[0]} — {branch_salary.iloc[0]:.2f} LPA")
        if len(cgpa_range_rate.dropna()):
            best_range = cgpa_range_rate.idxmax()
            insight_card("📈 CGPA Range with Best Placement Rate",
                         f"{best_range} — {cgpa_range_rate.max():.2f}%")
        if len(factor_corr):
            insight_card("⭐ Most Influential Experience Factor",
                         f"{factor_corr.index[0]} (correlation = {factor_corr.iloc[0]:.3f})")

    with col2:
        if len(company_counts):
            insight_card("🏢 Top Recruiting Company",
                         f"{company_counts.index[0]} — {company_counts.iloc[0]} students")
        max_sal = placed_df["Salary_Package_LPA"].max() if not placed_df.empty else 0
        insight_card("💵 Highest Salary Package", f"{max_sal:.2f} LPA")
        if len(salary_corr):
            insight_card("🔗 Strongest Correlation with Salary",
                         f"{salary_corr.index[0]} (correlation = {salary_corr.iloc[0]:.3f})")
        insight_card("✅ Overall Placement Rate", f"{placement_rate(df):.2f}%")

    st.markdown("---")
    st.markdown("**Correlation of Experience Factors with Placement**")
    fc = factor_corr.reset_index()
    fc.columns = ["Factor", "Correlation"]
    fig = px.bar(fc, x="Correlation", y="Factor", orientation="h",
                 color="Correlation", color_continuous_scale="Viridis")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)


# ===========================================================================
# PAGE 7 — DATASET EXPLORER
# ===========================================================================
elif page == "Dataset Explorer":
    st.subheader("🔎 Dataset Explorer")

    st.markdown("**Dataset Preview**")
    st.dataframe(df.drop(columns=["CGPA_Range"], errors="ignore"), use_container_width=True, height=320)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Dataset Shape**")
        st.write(f"Rows: {df.shape[0]}  |  Columns: {df.shape[1]}")

        st.markdown("**Column Data Types**")
        dtype_df = pd.DataFrame({"Column": df.dtypes.index.astype(str), "Data Type": df.dtypes.values.astype(str)})
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("**Missing Values Summary**")
        missing_df = df.isnull().sum().reset_index()
        missing_df.columns = ["Column", "Missing Values"]
        st.dataframe(missing_df, use_container_width=True, hide_index=True)

    st.markdown("**Summary Statistics**")
    st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

    st.markdown("---")
    csv_data = df.drop(columns=["CGPA_Range"], errors="ignore").to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_student_data.csv",
        mime="text/csv",
    )

st.markdown("---")
st.caption("Student Performance & Placement Analytics · Built with Streamlit, Pandas & Plotly")
