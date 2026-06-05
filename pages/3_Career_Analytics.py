import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Career Analytics",
    page_icon="📈",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/education_career_success.csv")

df = load_data()

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("📈 Career Analytics Dashboard")
st.markdown("Analyze career growth, salary trends, skills impact, and professional success.")

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------

st.sidebar.header("Filters")

if "Current_Job_Level" in df.columns:
    levels = st.sidebar.multiselect(
        "Job Level",
        options=df["Current_Job_Level"].dropna().unique(),
        default=df["Current_Job_Level"].dropna().unique()
    )

    df = df[df["Current_Job_Level"].isin(levels)]

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

if "Starting_Salary" in df.columns:
    avg_salary = df["Starting_Salary"].mean()

    col1.metric(
        "Average Salary",
        f"₹{avg_salary:,.0f}"
    )

if "Career_Satisfaction" in df.columns:
    satisfaction = df["Career_Satisfaction"].mean()

    col2.metric(
        "Career Satisfaction",
        f"{satisfaction:.2f}"
    )

if "Years_Experience" in df.columns:
    experience = df["Years_Experience"].mean()

    col3.metric(
        "Avg Experience",
        f"{experience:.1f} Years"
    )

col4.metric(
    "Total Records",
    len(df)
)

st.divider()

# -------------------------------------------------
# SALARY DISTRIBUTION
# -------------------------------------------------

if "Starting_Salary" in df.columns:

    st.subheader("💰 Salary Distribution")

    fig = px.histogram(
        df,
        x="Starting_Salary",
        nbins=30,
        title="Salary Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# GPA VS SALARY
# -------------------------------------------------

if (
    "University_GPA" in df.columns
    and "Starting_Salary" in df.columns
):

    st.subheader("🎓 GPA vs Salary")

    fig = px.scatter(
        df,
        x="University_GPA",
        y="Starting_Salary",
        color="Current_Job_Level"
        if "Current_Job_Level" in df.columns else None,
        size="Skills_Score"
        if "Skills_Score" in df.columns else None,
        hover_data=df.columns,
        title="Academic Performance vs Salary"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# JOB LEVEL DISTRIBUTION
# -------------------------------------------------

if "Current_Job_Level" in df.columns:

    st.subheader("🏆 Job Level Distribution")

    level_counts = (
        df["Current_Job_Level"]
        .value_counts()
        .reset_index()
    )

    level_counts.columns = [
        "Job Level",
        "Count"
    ]

    fig = px.bar(
        level_counts,
        x="Job Level",
        y="Count",
        text="Count"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# INTERNSHIP IMPACT
# -------------------------------------------------

if (
    "Internships_Completed" in df.columns
    and "Starting_Salary" in df.columns
):

    st.subheader("🏢 Internship Impact on Salary")

    fig = px.box(
        df,
        x="Internships_Completed",
        y="Starting_Salary"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# SKILLS IMPACT
# -------------------------------------------------

if (
    "Skills_Score" in df.columns
    and "Starting_Salary" in df.columns
):

    st.subheader("🚀 Skills vs Salary")

    fig = px.scatter(
        df,
        x="Skills_Score",
        y="Starting_Salary",
        color="Current_Job_Level"
        if "Current_Job_Level" in df.columns else None
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# NETWORKING IMPACT
# -------------------------------------------------

if (
    "Networking_Score" in df.columns
    and "Starting_Salary" in df.columns
):

    st.subheader("🤝 Networking Score vs Salary")

    fig = px.scatter(
        df,
        x="Networking_Score",
        y="Starting_Salary",
        color="Current_Job_Level"
        if "Current_Job_Level" in df.columns else None
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# CAREER SATISFACTION
# -------------------------------------------------

if "Career_Satisfaction" in df.columns:

    st.subheader("😊 Career Satisfaction")

    fig = px.histogram(
        df,
        x="Career_Satisfaction",
        nbins=20
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# SUCCESS SCORE
# -------------------------------------------------

required_cols = [
    "Skills_Score",
    "Networking_Score",
    "Internships_Completed",
    "Projects_Completed"
]

if all(col in df.columns for col in required_cols):

    st.subheader("⭐ Career Success Score")

    df["Career_Success_Score"] = (
        df["Skills_Score"] * 0.30 +
        df["Networking_Score"] * 0.25 +
        df["Internships_Completed"] * 0.25 +
        df["Projects_Completed"] * 0.20
    )

    avg_score = df["Career_Success_Score"].mean()

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=avg_score,
            title={"text": "Average Career Success Score"}
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# CORRELATION HEATMAP
# -------------------------------------------------

st.subheader("📊 Correlation Heatmap")

numeric_df = df.select_dtypes(include="number")

if len(numeric_df.columns) > 1:

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# RAW DATA
# -------------------------------------------------

st.subheader("📋 Career Dataset")

st.dataframe(
    df,
    use_container_width=True
)

# -------------------------------------------------
# DOWNLOAD
# -------------------------------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Career Analytics Data",
    data=csv,
    file_name="career_analytics.csv",
    mime="text/csv"
)
