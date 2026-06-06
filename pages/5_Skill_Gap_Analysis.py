import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Skill Gap Analysis", layout="wide")

st.title("📊 Skill Gap Analysis Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/Job_Placement_Data_Enhanced.csv")
    return df

df = load_data()

st.subheader("Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# FIX: HANDLE MISSING COLUMNS
# -----------------------------

required_columns = ["CGPA", "IQ", "Communication_Skills", "Technical_Skills"]

for col in required_columns:
    if col not in df.columns:
        st.warning(f"Missing column detected: {col} → Creating default values")
        df[col] = 0

# Create Skills_Score if missing
if "Skills_Score" not in df.columns:
    st.info("Skills_Score not found → Generating from existing features")

    df["Skills_Score"] = (
        df["Communication_Skills"] +
        df["Technical_Skills"]
    ) / 2

# -----------------------------
# SKILL GAP ANALYSIS
# -----------------------------

st.subheader("📉 Skill Score Distribution")

fig1 = px.histogram(
    df,
    x="Skills_Score",
    nbins=20,
    title="Distribution of Skills Score"
)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# SKILL vs PLACEMENT (if exists)
# -----------------------------

if "Placement_Status" in df.columns:
    st.subheader("🎯 Skills vs Placement")

    fig2 = px.box(
        df,
        x="Placement_Status",
        y="Skills_Score",
        color="Placement_Status",
        title="Skill Score vs Placement Status"
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Placement_Status column not found in dataset")

# -----------------------------
# TOP STUDENTS ANALYSIS
# -----------------------------

st.subheader("🏆 Top Students by Skills Score")

top_students = df.sort_values(by="Skills_Score", ascending=False).head(10)
st.dataframe(top_students)

# -----------------------------
# SKILL GAP INSIGHT
# -----------------------------

st.subheader("📌 Insights")

avg_score = df["Skills_Score"].mean()

st.write(f"📊 Average Skills Score: **{avg_score:.2f}**")

if avg_score < 50:
    st.error("⚠️ Overall skill level is LOW → Training required")
elif avg_score < 75:
    st.warning("⚠️ Moderate skill level → Improvement needed")
else:
    st.success("✅ Good skill level across students")

# -----------------------------
# OPTIONAL: DOWNLOAD DATA
# -----------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Processed Data",
    data=csv,
    file_name="skill_gap_analysis.csv",
    mime="text/csv"
)
