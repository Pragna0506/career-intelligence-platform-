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
# PATH SETUP
# =========================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# =========================
# LOAD MODELS
# =========================
salary_model = joblib.load(os.path.join(MODEL_DIR, "salary_model.pkl"))
placement_model = joblib.load(os.path.join(MODEL_DIR, "placement_model.pkl"))

# =========================
# INPUT UI
# =========================
st.subheader("📋 Student Profile")

age = st.slider("Age", 18, 40, 22)
gpa = st.slider("GPA", 0.0, 10.0, 5.0)
skills = st.slider("Skills Score", 0, 10, 5)
internships = st.slider("Internships", 0, 10, 0)
projects = st.slider("Projects", 0, 20, 0)
certifications = st.slider("Certifications", 0, 10, 0)
networking = st.slider("Networking Score", 0, 10, 5)

degree = st.selectbox("Degree", ["BTech", "BSc", "MBA", "BCA"])
gender = st.selectbox("Gender", ["Male", "Female"])
college_name = st.text_input("College Name", "Unknown")

# =========================
# BUTTON (IMPORTANT)
# =========================
if st.button("🚀 Predict Career Outcome"):

    # =========================
    # BUILD FULL FEATURE VECTOR
    # =========================
    input_data = pd.DataFrame([{
        "age": age,
        "gpa": gpa,
        "skills": skills,
        "internships": internships,
        "projects": projects,
        "certifications": certifications,
        "networking": networking,
        "degree": degree,
        "gender": gender,
        "college_name": college_name
    }])

    # Fill missing columns (VERY IMPORTANT)
    for col in salary_model.feature_names_in_:
        if col not in input_data.columns:
            input_data[col] = 0

    # reorder columns
    input_data = input_data[salary_model.feature_names_in_]

    st.write("📊 Final Input Shape:", input_data.shape)

    # =========================
    # SALARY PREDICTION
    # =========================
    st.subheader("💰 Salary Prediction")

    try:
        salary_pred = salary_model.predict(input_data)[0]
        st.success(f"💰 Predicted Salary: {salary_pred:.2f}")
    except Exception as e:
        st.error(f"Salary prediction failed: {e}")

    # =========================
    # PLACEMENT PREDICTION
    # =========================
    st.subheader("🎯 Placement Prediction")

    try:
        placement_pred = placement_model.predict(input_data)[0]

        if placement_pred >= 0.5:
            st.success("🎯 High Chance of Placement")
        else:
            st.warning("⚠️ Low Chance of Placement")

    except Exception as e:
        st.error(f"Placement prediction failed: {e}")

    # =========================
    # CAREER SCORE
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
