import streamlit as st
import pandas as pd
import glob
import plotly.express as px

st.set_page_config(page_title="Skill Gap Analysis", layout="wide")

st.title("📊 Skill Gap Analysis Dashboard")

# -----------------------------
# AUTO CSV LOADER (100% SAFE)
# -----------------------------
@st.cache_data
def load_data():

    csv_files = glob.glob("**/*.csv", recursive=True)

    if len(csv_files) == 0:
        st.error("❌ No CSV file found. Please upload dataset.")
        return None

    file_path = None

    for f in csv_files:
        if "dma" in f.lower() or "job" in f.lower():
            file_path = f
            break

    if file_path is None:
        file_path = csv_files[0]

    df = pd.read_csv(file_path)

    st.success(f"✅ Dataset loaded: {file_path}")

    return df


df = load_data()

if df is None:
    st.stop()

# -----------------------------
# CLEAN COLUMN NAMES
# -----------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# -----------------------------
# HANDLE MISSING COLUMNS
# -----------------------------
if "technical_skills" not in df.columns:
    df["technical_skills"] = 0

if "communication_skills" not in df.columns:
    df["communication_skills"] = 0

# -----------------------------
# SKILL SCORE
# -----------------------------
df["skills_score"] = (
    df["technical_skills"] +
    df["communication_skills"]
) / 2

# -----------------------------
# DASHBOARD
# -----------------------------
st.subheader("📉 Skill Distribution")

fig1 = px.histogram(df, x="skills_score", nbins=20)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🏆 Top Candidates")

st.dataframe(df.sort_values("skills_score", ascending=False).head(10))

st.subheader("📌 Insight")

avg = df["skills_score"].mean()

st.write(f"Average Skill Score: **{avg:.2f}**")

if avg < 50:
    st.error("Low skill level → Training needed")
elif avg < 75:
    st.warning("Medium skill level → Improve skills")
else:
    st.success("Good skill level")
