import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Skill Gap Analysis",
    page_icon="🎯",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv("data3/education_career_success.csv")

df = load_data()

# ==========================================================
# TITLE
# ==========================================================

st.title("🎯 Skill Gap Analysis")
st.markdown(
    "Identify strengths, weaknesses, career readiness, and improvement opportunities."
)

# ==========================================================
# REQUIRED COLUMNS CHECK
# ==========================================================

required_cols = [
    "Skills_Score",
    "Networking_Score",
    "Projects_Completed",
    "Internships_Completed"
]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(
        f"Missing required columns: {', '.join(missing)}"
    )
    st.stop()

# ==========================================================
# CAREER READINESS SCORE
# ==========================================================

df["Career_Readiness_Score"] = (
    df["Skills_Score"] * 0.35 +
    df["Networking_Score"] * 0.25 +
    df["Projects_Completed"] * 0.20 +
    df["Internships_Completed"] * 0.20
)

# ==========================================================
# KPI SECTION
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Skill Score",
    f"{df['Skills_Score'].mean():.2f}"
)

col2.metric(
    "Average Networking",
    f"{df['Networking_Score'].mean():.2f}"
)

col3.metric(
    "Avg Internships",
    f"{df['Internships_Completed'].mean():.2f}"
)

col4.metric(
    "Career Readiness",
    f"{df['Career_Readiness_Score'].mean():.2f}"
)

st.divider()

# ==========================================================
# CAREER READINESS DISTRIBUTION
# ==========================================================

st.subheader("📊 Career Readiness Distribution")

fig = px.histogram(
    df,
    x="Career_Readiness_Score",
    nbins=30,
    title="Career Readiness Score Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# SKILL SCORE DISTRIBUTION
# ==========================================================

st.subheader("🚀 Skill Score Distribution")

fig = px.box(
    df,
    y="Skills_Score"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# NETWORKING ANALYSIS
# ==========================================================

st.subheader("🤝 Networking Score Analysis")

fig = px.histogram(
    df,
    x="Networking_Score",
    nbins=20
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# INTERNSHIP IMPACT
# ==========================================================

st.subheader("🏢 Internship Contribution")

internship_counts = (
    df["Internships_Completed"]
    .value_counts()
    .reset_index()
)

internship_counts.columns = [
    "Internships",
    "Count"
]

fig = px.bar(
    internship_counts,
    x="Internships",
    y="Count",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# PROJECT CONTRIBUTION
# ==========================================================

if "Projects_Completed" in df.columns:

    st.subheader("📁 Projects Contribution")

    fig = px.histogram(
        df,
        x="Projects_Completed",
        nbins=20
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# RADAR CHART
# ==========================================================

st.subheader("🕸 Average Competency Radar")

avg_skill = df["Skills_Score"].mean()
avg_network = df["Networking_Score"].mean()
avg_projects = df["Projects_Completed"].mean()
avg_internships = df["Internships_Completed"].mean()

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=[
            avg_skill,
            avg_network,
            avg_projects,
            avg_internships
        ],
        theta=[
            "Skills",
            "Networking",
            "Projects",
            "Internships"
        ],
        fill="toself"
    )
)

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# GAP IDENTIFICATION
# ==========================================================

st.subheader("⚠ Skill Gap Identification")

threshold = st.slider(
    "Gap Threshold",
    min_value=1,
    max_value=10,
    value=6
)

skill_gap = {}

for col in [
    "Skills_Score",
    "Networking_Score"
]:
    skill_gap[col] = (df[col] < threshold).sum()

gap_df = pd.DataFrame({
    "Category": list(skill_gap.keys()),
    "Students_Below_Threshold": list(skill_gap.values())
})

fig = px.bar(
    gap_df,
    x="Category",
    y="Students_Below_Threshold",
    text_auto=True,
    title="Students Below Desired Threshold"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# STUDENT SEGMENTATION
# ==========================================================

st.subheader("🏅 Career Readiness Segmentation")

conditions = [
    df["Career_Readiness_Score"] >= 8,
    (df["Career_Readiness_Score"] >= 6) &
    (df["Career_Readiness_Score"] < 8),
    df["Career_Readiness_Score"] < 6
]

choices = [
    "High Potential",
    "Moderate Potential",
    "Needs Improvement"
]

df["Segment"] = np.select(
    conditions,
    choices,
    default="Needs Improvement"
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
    values="Count",
    title="Career Readiness Segments"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# RECOMMENDATIONS
# ==========================================================

st.subheader("💡 Recommendations")

avg_skill = df["Skills_Score"].mean()
avg_network = df["Networking_Score"].mean()

recommendations = []

if avg_skill < 6:
    recommendations.append(
        "Improve technical skills through projects and certifications."
    )

if avg_network < 6:
    recommendations.append(
        "Participate in networking events and professional communities."
    )

if df["Internships_Completed"].mean() < 2:
    recommendations.append(
        "Encourage students to complete additional internships."
    )

if df["Projects_Completed"].mean() < 3:
    recommendations.append(
        "Increase project-based learning opportunities."
    )

if recommendations:
    for item in recommendations:
        st.warning(item)
else:
    st.success(
        "No major skill gaps detected. Overall readiness is strong."
    )

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

st.subheader("📈 Correlation Analysis")

numeric_df = df.select_dtypes(include="number")

corr = numeric_df.corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# DATA TABLE
# ==========================================================

st.subheader("📋 Dataset Preview")

st.dataframe(
    df.head(50),
    use_container_width=True
)

# ==========================================================
# DOWNLOAD
# ==========================================================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Skill Gap Report",
    data=csv,
    file_name="skill_gap_analysis.csv",
    mime="text/csv"
)
