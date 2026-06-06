import streamlit as st
import pandas as pd
import glob
import os
import plotly.express as px

st.set_page_config(page_title="Skill Gap Analysis", layout="wide")

st.title("📊 Skill Gap Analysis Dashboard")

# -----------------------------
# FAST AUTO DATA LOADER (NO PATH ISSUES)
# -----------------------------
@st.cache_data
def load_data():

    # Try to find ANY CSV in data folder
    csv_files = glob.glob("data/*.csv")

    # If not found, try root folder
    if len(csv_files) == 0:
        csv_files = glob.glob("*.csv")

    if len(csv_files) == 0:
        st.error("❌ No dataset found in project!")
        return None

    file_path = csv_files[0]  # take first available file

    st.success(f"✅ Dataset loaded: {file_path}")

    return pd.read_csv(file_path)


df = load_data()

if df is None:
    st.stop()

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.subheader("Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# AUTO FEATURE FIX
# -----------------------------
if "Communication_Skills" not in df.columns:
    df["Communication_Skills"] = 0

if "Technical_Skills" not in df.columns:
    df["Technical_Skills"] = 0

# -----------------------------
# CREATE SKILL SCORE
# -----------------------------
if "Skills_Score" not in df.columns:
    df["Skills_Score"] = (
        df["Communication_Skills"] +
        df["Technical_Skills"]
    ) / 2

# -----------------------------
# CHART 1
# -----------------------------
st.subheader("📉 Skill Distribution")

fig1 = px.histogram(df, x="Skills_Score", nbins=20)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# CHART 2
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
# INSIGHT
# -----------------------------
st.subheader("📌 Insight")

avg = df["Skills_Score"].mean()

st.write("Average Skill Score:", round(avg, 2))

if avg < 50:
    st.error("Low skill level → Needs training")
elif avg < 75:
    st.warning("Medium skill level → Improve")
else:
    st.success("Good skill level")
