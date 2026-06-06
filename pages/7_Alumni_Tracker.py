import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Alumni Career Tracker",
    page_icon="🎓",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "data3/education_career_success.csv"
    )

df = load_data()

# ==========================================================
# TITLE
# ==========================================================

st.title("🎓 Alumni Career Tracker")

st.markdown("""
Track alumni growth, career progression,
salary trends, promotions, and success indicators.
""")

st.divider()

# ==========================================================
# CREATE GROWTH SCORE
# ==========================================================

required_cols = [
    "Skills_Score",
    "Networking_Score",
    "Internships_Completed",
    "Projects_Completed"
]

if all(col in df.columns for col in required_cols):

    df["Career_Growth_Score"] = (
        df["Skills_Score"] * 0.35 +
        df["Networking_Score"] * 0.25 +
        df["Internships_Completed"] * 0.20 +
        df["Projects_Completed"] * 0.20
    )

# ==========================================================
# KPI SECTION
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Alumni",
    len(df)
)

if "Starting_Salary" in df.columns:
    col2.metric(
        "Average Salary",
        f"₹{df['Starting_Salary'].mean():,.0f}"
    )

if "Career_Satisfaction" in df.columns:
    col3.metric(
        "Career Satisfaction",
        f"{df['Career_Satisfaction'].mean():.2f}/10"
    )

if "Career_Growth_Score" in df.columns:
    col4.metric(
        "Growth Score",
        f"{df['Career_Growth_Score'].mean():.2f}"
    )

st.divider()

# ==========================================================
# JOB LEVEL DISTRIBUTION
# ==========================================================

if "Current_Job_Level" in df.columns:

    st.subheader("🏆 Alumni by Job Level")

    fig = px.histogram(
        df,
        x="Current_Job_Level",
        color="Current_Job_Level",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# SALARY DISTRIBUTION
# ==========================================================

if "Starting_Salary" in df.columns:

    st.subheader("💰 Salary Distribution")

    fig = px.histogram(
        df,
        x="Starting_Salary",
        nbins=40,
        marginal="box"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# GPA VS SALARY
# ==========================================================

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
        if "Current_Job_Level" in df.columns
        else None,
        size="Skills_Score"
        if "Skills_Score" in df.columns
        else None,
        hover_data=df.columns
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# CAREER SATISFACTION
# ==========================================================

if "Career_Satisfaction" in df.columns:

    st.subheader("😊 Career Satisfaction")

    fig = px.histogram(
        df,
        x="Career_Satisfaction",
        nbins=20
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# EXPERIENCE ANALYSIS
# ==========================================================

if "Years_Experience" in df.columns:

    st.subheader("📈 Experience Distribution")

    fig = px.box(
        df,
        y="Years_Experience"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# FIELD OF STUDY ANALYSIS
# ==========================================================

if "Field_of_Study" in df.columns:

    st.subheader("📚 Alumni by Field of Study")

    field_df = (
        df["Field_of_Study"]
        .value_counts()
        .reset_index()
    )

    field_df.columns = [
        "Field",
        "Count"
    ]

    fig = px.bar(
        field_df,
        x="Field",
        y="Count",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# TOP PERFORMERS
# ==========================================================

if (
    "Career_Growth_Score" in df.columns
):

    st.subheader("🥇 Top Alumni")

    top_alumni = (
        df.sort_values(
            "Career_Growth_Score",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_alumni,
        use_container_width=True
    )

# ==========================================================
# ALUMNI SEGMENTATION
# ==========================================================

if "Career_Growth_Score" in df.columns:

    st.subheader("🏅 Alumni Segmentation")

    conditions = [
        df["Career_Growth_Score"] >= 8,
        (
            (df["Career_Growth_Score"] >= 6) &
            (df["Career_Growth_Score"] < 8)
        ),
        df["Career_Growth_Score"] < 6
    ]

    choices = [
        "High Performers",
        "Emerging Talent",
        "Needs Support"
    ]

    df["Segment"] = np.select(
        conditions,
        choices,
        default="Needs Support"
    )

    segment_df = (
        df["Segment"]
        .value_counts()
        .reset_index()
    )

    segment_df.columns = [
        "Segment",
        "Count"
    ]

    fig = px.pie(
        segment_df,
        names="Segment",
        values="Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# CAREER GROWTH GAUGE
# ==========================================================

if "Career_Growth_Score" in df.columns:

    st.subheader("🚀 Average Career Growth")

    avg_growth = (
        df["Career_Growth_Score"]
        .mean()
    )

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=avg_growth,
            title={
                "text":
                "Career Growth Score"
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

st.subheader("📊 Correlation Analysis")

numeric_df = df.select_dtypes(
    include="number"
)

if len(numeric_df.columns) > 1:

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# CAREER INSIGHTS
# ==========================================================

st.subheader("🔍 Alumni Insights")

insights = []

if "Starting_Salary" in df.columns:
    insights.append(
        f"Average Salary: ₹{df['Starting_Salary'].mean():,.0f}"
    )

if "Career_Satisfaction" in df.columns:
    insights.append(
        f"Average Satisfaction: {df['Career_Satisfaction'].mean():.2f}/10"
    )

if "Years_Experience" in df.columns:
    insights.append(
        f"Average Experience: {df['Years_Experience'].mean():.1f} years"
    )

for item in insights:
    st.info(item)

# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

st.subheader("📥 Export Data")

csv = df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Alumni Report",
    data=csv,
    file_name="alumni_tracker_report.csv",
    mime="text/csv"
)

# ==========================================================
# RAW DATA
# ==========================================================

st.subheader("📋 Alumni Dataset")

st.dataframe(
    df.head(100),
    use_container_width=True
)
