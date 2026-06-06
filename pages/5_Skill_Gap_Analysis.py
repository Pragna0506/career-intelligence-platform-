import streamlit as st
import pandas as pd
import glob
import os
import plotly.express as px

st.set_page_config(page_title="Skill Gap Analysis", layout="wide")

st.title("📊 Skill Gap Analysis Dashboard")

# -----------------------------
# DEBUG: SHOW ALL FILES (VERY IMPORTANT)
# -----------------------------
st.sidebar.subheader("📁 Debug - Files in Project")

all_files = []
for root, dirs, files in os.walk("."):
    for f in files:
        all_files.append(os.path.join(root, f))

st.sidebar.write(all_files)

# -----------------------------
# SMART DATA LOADER (100% SAFE)
# -----------------------------
@st.cache_data
def load_data():

    # Try all CSV files in project
    csv_files = glob.glob("**/*.csv", recursive=True)

    if len(csv_files) == 0:
        return None, None

    # Prefer job placement file if exists
    preferred = None
    for f in csv_files:
        if "job" in f.lower() and "placement" in f.lower():
            preferred = f
            break

    file_path = preferred if preferred else csv_files[0]

    df = pd.read_csv(file_path)

    return df, file_path


df, file_path = load_data()

# -----------------------------
# ERROR HANDLING
# -----------------------------
if df is None:
    st.error("❌ No CSV file found anywhere in project!")
    st.stop()

st.success(f"✅ Dataset loaded successfully: {file_path}")

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
# INSIGHT
# -----------------------------
st.subheader("📌 Insights")

avg = df["Skills_Score"].mean()

st.write("Average Skill Score:", round(avg, 2))

if avg < 50:
    st.error("Low skill level → Training needed")
elif avg < 75:
    st.warning("Medium skill level → Improve skills")
else:
    st.success("Good skill level")
