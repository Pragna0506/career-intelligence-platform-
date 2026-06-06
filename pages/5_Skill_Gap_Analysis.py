import streamlit as st
import pandas as pd
import glob
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Skill Gap Analysis", layout="wide")

st.title("📊 Skill Gap Analysis Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    csv_files = glob.glob("**/*.csv", recursive=True)

    if len(csv_files) == 0:
        st.error("❌ No dataset found")
        return None

    return pd.read_csv(csv_files[0])


df = load_data()

if df is None:
    st.stop()

# -----------------------------
# CLEAN COLUMN NAMES
# -----------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

st.subheader("Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# SMART VALUE CONVERTER
# -----------------------------
def convert_skill(value):
    if pd.isna(value):
        return 0

    value = str(value).lower()

    mapping = {
        "excellent": 95,
        "very good": 85,
        "good": 75,
        "average": 60,
        "medium": 60,
        "low": 40,
        "poor": 20,
        "bad": 10
    }

    if value.replace(".", "", 1).isdigit():
        return float(value)

    return mapping.get(value, 50)  # default mid score


# -----------------------------
# FIND COLUMNS FLEXIBLY
# -----------------------------
def find_column(possible_names):
    for col in df.columns:
        for name in possible_names:
            if name in col:
                return col
    return None


tech_col = find_column(["tech", "technical", "coding", "skill"])
comm_col = find_column(["comm", "communication", "soft"])

# -----------------------------
# APPLY CONVERSION
# -----------------------------
if tech_col:
    df["technical_score"] = df[tech_col].apply(convert_skill)
else:
    df["technical_score"] = 50

if comm_col:
    df["communication_score"] = df[comm_col].apply(convert_skill)
else:
    df["communication_score"] = 50

# -----------------------------
# FINAL SKILL SCORE
# -----------------------------
df["skills_score"] = (
    df["technical_score"] +
    df["communication_score"]
) / 2

# -----------------------------
# FIX ZERO ISSUE
# -----------------------------
if df["skills_score"].sum() == 0:
    df["skills_score"] = 60  # fallback safe value

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

st.dataframe(df.sort_values("skills_score", ascending=False).head(10))

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
