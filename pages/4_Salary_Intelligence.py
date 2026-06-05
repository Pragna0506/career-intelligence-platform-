import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Salary Intelligence",
    page_icon="💰",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/education_career_success.csv")

df = load_data()

# =====================================================
# TITLE
# =====================================================

st.title("💰 Salary Intelligence Dashboard")
st.markdown(
    "Analyze salary trends, career growth factors, and compensation insights."
)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Filters")

if "Current_Job_Level" in df.columns:
    levels = st.sidebar.multiselect(
        "Job Level",
        options=df["Current_Job_Level"].dropna().unique(),
        default=df["Current_Job_Level"].dropna().unique()
    )

    df = df[df["Current_Job_Level"].isin(levels)]

# =====================================================
# KPI SECTION
# =====================================================

col1, col2, col3, col4 = st.columns(4)

if "Starting_Salary" in df.columns:

    col1.metric(
        "Average Salary",
        f"₹{df['Starting_Salary'].mean():,.0f}"
    )

    col2.metric(
        "Maximum Salary",
        f"₹{df['Starting_Salary'].max():,.0f}"
    )

    col3.metric(
        "Minimum Salary",
        f"₹{df['Starting_Salary'].min():,.0f}"
    )

    col4.metric(
        "Salary Median",
        f"₹{df['Starting_Salary'].median():,.0f}"
    )

st.divider()

# =====================================================
# SALARY DISTRIBUTION
# =====================================================

if "Starting_Salary" in df.columns:

    st.subheader("📊 Salary Distribution")

    fig = px.histogram(
        df,
        x="Starting_Salary",
        nbins=40,
        marginal="box",
        title="Salary Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# GPA VS SALARY
# =====================================================

if (
    "University_GPA" in df.columns and
    "Starting_Salary" in df.columns
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
        hover_data=df.columns
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# INTERNSHIPS VS SALARY
# =====================================================

if (
    "Internships_Completed" in df.columns and
    "Starting_Salary" in df.columns
):

    st.subheader("🏢 Internships Impact on Salary")

    fig = px.box(
        df,
        x="Internships_Completed",
        y="Starting_Salary"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# PROJECTS VS SALARY
# =====================================================

if (
    "Projects_Completed" in df.columns and
    "Starting_Salary" in df.columns
):

    st.subheader("📁 Projects Impact on Salary")

    fig = px.scatter(
        df,
        x="Projects_Completed",
        y="Starting_Salary",
        color="Current_Job_Level"
        if "Current_Job_Level" in df.columns else None
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# SKILLS SCORE VS SALARY
# =====================================================

if (
    "Skills_Score" in df.columns and
    "Starting_Salary" in df.columns
):

    st.subheader("🚀 Skills Score vs Salary")

    fig = px.scatter(
        df,
        x="Skills_Score",
        y="Starting_Salary",
        color="Current_Job_Level"
        if "Current_Job_Level" in df.columns else None
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# NETWORKING SCORE VS SALARY
# =====================================================

if (
    "Networking_Score" in df.columns and
    "Starting_Salary" in df.columns
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

# =====================================================
# JOB LEVEL SALARY ANALYSIS
# =====================================================

if (
    "Current_Job_Level" in df.columns and
    "Starting_Salary" in df.columns
):

    st.subheader("🏆 Salary by Job Level")

    salary_level = (
        df.groupby("Current_Job_Level")["Starting_Salary"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        salary_level,
        x="Current_Job_Level",
        y="Starting_Salary",
        text_auto=".2s"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# TOP EARNERS
# =====================================================

if "Starting_Salary" in df.columns:

    st.subheader("🥇 Top 10 Highest Salaries")

    top_salary = (
        df.sort_values(
            by="Starting_Salary",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_salary,
        use_container_width=True
    )

# =====================================================
# SALARY PREDICTOR
# =====================================================

st.subheader("🧠 Salary Intelligence Score")

required_cols = [
    "Skills_Score",
    "Networking_Score",
    "Internships_Completed",
    "Projects_Completed"
]

if all(col in df.columns for col in required_cols):

    df["Salary_Potential_Score"] = (
        df["Skills_Score"] * 0.35 +
        df["Networking_Score"] * 0.25 +
        df["Internships_Completed"] * 0.20 +
        df["Projects_Completed"] * 0.20
    )

    avg_score = df["Salary_Potential_Score"].mean()

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=avg_score,
            title={"text": "Average Salary Potential Score"}
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# CORRELATION HEATMAP
# =====================================================

st.subheader("📈 Salary Correlation Heatmap")

numeric_df = df.select_dtypes(include="number")

if len(numeric_df.columns) > 1:

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# INSIGHTS
# =====================================================

st.subheader("🔍 Key Insights")

if "Starting_Salary" in df.columns:

    st.info(
        f"""
        • Average Salary: ₹{df['Starting_Salary'].mean():,.0f}

        • Highest Salary: ₹{df['Starting_Salary'].max():,.0f}

        • Lowest Salary: ₹{df['Starting_Salary'].min():,.0f}

        • Salary Range: ₹{df['Starting_Salary'].max()-df['Starting_Salary'].min():,.0f}
        """
    )

# =====================================================
# DOWNLOAD DATA
# =====================================================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Salary Analytics",
    data=csv,
    file_name="salary_intelligence.csv",
    mime="text/csv"
)
