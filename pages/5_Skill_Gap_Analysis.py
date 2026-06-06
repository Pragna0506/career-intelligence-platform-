import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="Skill Gap Analysis", layout="wide")

st.title("📊 Skill Gap Analysis Dashboard")

# -----------------------------
# LOAD EXCEL FILE (FIXED)
# -----------------------------
@st.cache_data
def load_data():

    file_path = "data/DMA DATASET.xlsx"

    # check file exists
    if not os.path.exists(file_path):
        st.error(f"""
❌ Dataset not found!

Expected file:
{file_path}

👉 FIX:
- Make sure file is inside /data folder
- File name must be EXACT: DMA DATASET.xlsx
        """)
        return None

    # read excel file
    df = pd.read_excel(file_path)

    return df


df = load_data()

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
if "Communication_Skills" not in df.columns:
    df["Communication_Skills"] = 0

if "Technical_Skills" not in df.columns:
    df["Technical_Skills"] = 0

# -----------------------------
# CREATE SKILLS SCORE
# -----------------------------
if "Skills_Score" not in df.columns:
    df["Skills_Score"] = (
        df["Communication_Skills"] +
        df["Technical_Skills"]
    ) / 2

# -----------------------------
# VISUALIZATION
# -----------------------------
st.subheader("📉 Skill Score Distribution")

fig1 = px.histogram(df, x="Skills_Score", nbins=20)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# PLACEMENT ANALYSIS
# -----------------------------
if "Placement_Status" in df.columns:
    st.subheader("🎯 Skills vs Placement")

    fig2 = px.box(
        df,
        x="Placement_Status",
        y="Skills_Score",
        color="Placement_Status"
    )
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# TOP STUDENTS
# -----------------------------
st.subheader("🏆 Top Students")

st.dataframe(df.sort_values("Skills_Score", ascending=False).head(10))

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("📌 Insights")

avg = df["Skills_Score"].mean()

st.write(f"Average Skill Score: {avg:.2f}")

if avg < 50:
    st.error("Low skill level → Training required")
elif avg < 75:
    st.warning("Medium skill level → Improve skills")
else:
    st.success("Good skill level")
