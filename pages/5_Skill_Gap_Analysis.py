import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="Skill Gap Analysis", layout="wide")

st.title("📊 Skill Gap Analysis Dashboard")

# -----------------------------
# SAFE DATA LOADING
# -----------------------------
@st.cache_data
def load_data():
    file_path = "data/job_Placement.csv"

    # ✅ CHECK IF FILE EXISTS
    if not os.path.exists(file_path):
        st.error(f"""
        ❌ Dataset not found!

        Expected path:
        `{file_path}`

        👉 Fix:
        - Check if file is inside /data folder
        - Check spelling and file name
        """)
        return None

    df = pd.read_csv(file_path)
    return df


df = load_data()

# STOP EXECUTION IF DATA NOT FOUND
if df is None:
    st.stop()

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.subheader("Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# SAFE COLUMN HANDLING
# -----------------------------
for col in ["Communication_Skills", "Technical_Skills"]:
    if col not in df.columns:
        df[col] = 0

# -----------------------------
# CREATE SKILLS SCORE
# -----------------------------
if "Skills_Score" not in df.columns:
    df["Skills_Score"] = (
        df["Communication_Skills"] +
        df["Technical_Skills"]
    ) / 2

# -----------------------------
# ANALYSIS
# -----------------------------
st.subheader("📉 Skills Score Distribution")

fig1 = px.histogram(
    df,
    x="Skills_Score",
    nbins=20,
    title="Skills Score Distribution"
)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# PLACEMENT ANALYSIS (SAFE)
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
    st.warning("Placement_Status column not found")

# -----------------------------
# TOP STUDENTS
# -----------------------------
st.subheader("🏆 Top Students")

top = df.sort_values("Skills_Score", ascending=False).head(10)
st.dataframe(top)

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("📌 Insights")

avg = df["Skills_Score"].mean()

st.write(f"Average Skill Score: **{avg:.2f}**")

if avg < 50:
    st.error("Low skill level → Training required")
elif avg < 75:
    st.warning("Moderate skill level → Improvement needed")
else:
    st.success("Good skill level")
