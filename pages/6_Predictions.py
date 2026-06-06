import streamlit as st
import numpy as np
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
# PATH FIX (IMPORTANT)
# =========================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# =========================
# LOAD MODELS
# =========================
try:
    salary_model = joblib.load(os.path.join(MODEL_DIR, "salary_model.pkl"))
    placement_model = joblib.load(os.path.join(MODEL_DIR, "placement_model.pkl"))
except Exception as e:
    st.error(f"❌ Model loading failed: {e}")
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
# BASE INPUT (5 FEATURES)
# =========================
base_input = [
    gpa,
    skills,
    networking,
    internships,
    projects
]

# =========================
# FIXED INPUT FOR MODELS
# =========================

# 🔥 SALARY MODEL → 16 FEATURES
salary_input = np.array([base_input * 3 + [gpa]])  # 15 + 1 = 16

# 🔥 PLACEMENT MODEL → 7 FEATURES
placement_input = np.array([base_input[:5] + [gpa, skills]])  # 7 features

# =========================
# SHOW INPUT
# =========================
st.write("📊 Base Input:", base_input)

# =========================
# SALARY PREDICTION
# =========================
st.subheader("💰 Salary Prediction")

try:
    salary_pred = salary_model.predict(salary_input)[0]
    st.success(f"💰 Predicted Salary: {salary_pred:.2f}")
except Exception as e:
    st.error(f"Salary prediction failed: {e}")

# =========================
# PLACEMENT PREDICTION
# =========================
st.subheader("🎯 Placement Prediction")

try:
    placement_pred = placement_model.predict(placement_input)[0]

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

st.success("🚀 Keep improving for better career opportunities!")
