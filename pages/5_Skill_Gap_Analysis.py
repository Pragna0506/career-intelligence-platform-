import streamlit as st
import pandas as pd
import glob
import os
import plotly.express as px

st.set_page_config(page_title="Skill Gap Analysis", layout="wide")

st.title("📊 Skill Gap Analysis Dashboard")

# -----------------------------
# AUTO DATA LOADER (NO PATH ISSUES)
# -----------------------------
@st.cache_data
def load_data():

    # Search ALL excel files in project
    excel_files = glob.glob("**/*.xlsx", recursive=True)

    if len(excel_files) == 0:
        st.error("❌ No Excel file found in project")
        return None

    # Prefer DMA dataset
    file_path = None
    for f in excel_files:
        if "dma" in f.lower():
            file_path = f
            break

    if file_path is None:
        file_path = excel_files[0]

    df = pd.read_excel(file_path)

    st.success(f"✅ Dataset loaded: {file_path}")

    return df


df = load_data()

if df is None:
    st.stop()

# -----------------------------
# CLEAN COLUMN NAMES (IMPORTANT FIX)
# -----------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.subheader("Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# HANDLE MISSING COLUMNS SAFELY
# -----------------------------
if "technical_skills" not in df.columns:
    df["technical_skills"] = 0

if "communication_skills" not in df.columns:
    df["communication_skills"] = 0

if "projects" not in df.columns:
    df["projects"] = 0

# -----------------------------
# CREATE SKILL SCORE
# -----------------------------
df["skills_score"] = (
    df["technical_skills"] +
    df["communication_skills"]
) / 2

# -----------------------------
# VISUALIZATION
# -----------------------------
st.subheader("📉 Skill Distribution")

fig1 = px.histogram(df, x="skills_score", nbins=20)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# TOP STUDENTS
# -----------------------------
st.subheader("🏆 Top Candidates")

top = df.sort_values("skills_score", ascending=False).head(10)
st.dataframe(top)

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("📌 Insights")

avg = df["skills_score"].mean()

st.write(f"Average Skill Score: **{avg:.2f}**")

if avg < 50:
    st.error("Low skill level → Training needed")
elif avg < 75:
    st.warning("Medium skill level → Improve skills")
else:
    st.success("Good skill level")
