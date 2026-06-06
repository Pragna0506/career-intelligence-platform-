import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Career Prediction Center",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Career Prediction Center")
st.markdown("Predict placement chances, salary, and career readiness.")

# =========================
# PATH SETUP (IMPORTANT FIX)
# =========================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# =========================
# LOAD MODELS + FEATURES
# =========================
try:
    salary_model = joblib.load(os.path.join(MODEL_DIR, "salary_model.pkl"))
    placement_model = joblib.load(os.path.join(MODEL_DIR, "placement_model.pkl"))
    feature_list = joblib.load(os.path.join(MODEL_DIR, "feature_list.pkl"))
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# =========================
# INPUT SECTION
# =========================
st.subheader("📋 Student Profile")

gpa = st.slider("University GPA", 0.0, 10.0, 5.0)
skills = st.slider("Skills Score", 0, 10, 5)
networking = st.slider("Networking Score", 0, 10, 5)
internships = st.slider("Internships Completed", 0, 10, 0)
projects = st.slider("Projects Completed", 0, 20, 0)

# =========================
# USER INPUT DICTIONARY
# =========================
user_data = {
    "University_GPA": gpa,
    "Skills": skills,
    "Networking_Score": networking,
    "Internships_Completed": internships,
    "Projects_Completed": projects
}

# =========================
# BUILD DATAFRAME MATCHING TRAINING FEATURES
# =========================
input_df = pd.DataFrame([user_data])

# Fill missing columns with 0
for col in feature_list:
    if col not in input_df.columns:
        input_df[col] = 0

# Reorder columns EXACTLY like training
input_df = input_df[feature_list]

st.write("📊 Final Input Shape:", input_df.shape)

# =========================
# SALARY PREDICTION
# =========================
st.subheader("💰 Salary Prediction")

try:
    salary_pred = salary_model.predict(input_df)[0]
    st.success(f"💰 Predicted Salary: {salary_pred:.2f}")
except Exception as e:
    st.error(f"Salary prediction failed: {e}")

# =========================
# PLACEMENT PREDICTION
# =========================
st.subheader("🎯 Placement Prediction")

try:
    placement_pred = placement_model.predict(input_df)[0]

    if placement_pred >= 0.5:
        st.success("🎯 High Chance of Placement")
    else:
        st.warning("⚠️ Low Chance of Placement")

except Exception as e:
    st.error(f"Placement prediction failed: {e}")

# =========================
# CAREER READINESS SCORE
# =========================
st.subheader("📊 Career Readiness")

score = (gpa * 10 + skills * 5 + networking * 5 + internships * 5 + projects * 2) / 10
score = min(score, 10)

st.metric("Career Score", f"{score:.1f}/10")

if score >= 7:
    st.success("Excellent profile 🚀")
elif score >= 4:
    st.info("Good profile 👍")
else:
    st.warning("Needs improvement ⚠️")

# =========================
# ROADMAP
# =========================
st.subheader("🛣 Career Roadmap")

if skills < 5:
    st.write("👉 Improve technical skills")

if internships < 2:
    st.write("👉 Do internships")

if networking < 5:
    st.write("👉 Improve networking")

if projects < 3:
    st.write("👉 Build more projects")

st.success("🚀 Keep improving for better opportunities!")
