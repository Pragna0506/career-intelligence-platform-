import streamlit as st
import pandas as pd
import joblib
import numpy as np

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Predictions",
    page_icon="🧠",
    layout="wide"
)

# ==========================================================
# LOAD MODELS
# ==========================================================

@st.cache_resource
def load_models():

    models = {}

    try:
        models["salary"] = joblib.load(
            "models/salary_model.pkl"
        )
    except:
        models["salary"] = None

    try:
        models["placement"] = joblib.load(
            "models/placement_model.pkl"
        )
    except:
        models["placement"] = None

    try:
        models["scaler"] = joblib.load(
            "models/scaler.pkl"
        )
    except:
        models["scaler"] = None

    return models

models = load_models()

# ==========================================================
# TITLE
# ==========================================================

st.title("🧠 Career Prediction Center")

st.markdown(
    """
    Predict placement chances, expected salary,
    and overall career readiness.
    """
)

st.divider()

# ==========================================================
# USER INPUTS
# ==========================================================

st.subheader("📋 Student Profile")

col1, col2 = st.columns(2)

with col1:

    gpa = st.slider(
        "University GPA",
        0.0,
        10.0,
        7.0
    )

    skills = st.slider(
        "Skills Score",
        0,
        10,
        6
    )

    networking = st.slider(
        "Networking Score",
        0,
        10,
        5
    )

with col2:

    internships = st.slider(
        "Internships Completed",
        0,
        10,
        2
    )

    projects = st.slider(
        "Projects Completed",
        0,
        20,
        4
    )

# ==========================================================
# FEATURE VECTOR
# ==========================================================

features = np.array([
    [
        gpa,
        skills,
        networking,
        internships,
        projects
    ]
])

# ==========================================================
# APPLY SCALER
# ==========================================================

if models["scaler"] is not None:

    try:
        features_scaled = (
            models["scaler"]
            .transform(features)
        )

    except:
        features_scaled = features

else:
    features_scaled = features

# ==========================================================
# PREDICT BUTTON
# ==========================================================

if st.button(
    "🚀 Generate Predictions",
    use_container_width=True
):

    st.divider()

    col1, col2, col3 = st.columns(3)

    # ======================================================
    # SALARY PREDICTION
    # ======================================================

    if models["salary"] is not None:

        try:

            salary = (
                models["salary"]
                .predict(features_scaled)[0]
            )

            col1.metric(
                "Predicted Salary",
                f"₹{salary:,.0f}"
            )

        except:

            col1.error(
                "Salary model prediction failed."
            )

    else:

        estimated_salary = (
            gpa * 50000 +
            skills * 70000 +
            networking * 30000 +
            internships * 50000 +
            projects * 10000
        )

        col1.metric(
            "Estimated Salary",
            f"₹{estimated_salary:,.0f}"
        )

    # ======================================================
    # PLACEMENT PREDICTION
    # ======================================================

    if models["placement"] is not None:

        try:

            placement = (
                models["placement"]
                .predict(features_scaled)[0]
            )

            if hasattr(
                models["placement"],
                "predict_proba"
            ):

                probability = (
                    models["placement"]
                    .predict_proba(
                        features_scaled
                    )[0]
                )

                confidence = (
                    max(probability) * 100
                )

            else:

                confidence = 80

            col2.metric(
                "Placement Prediction",
                str(placement)
            )

            col2.metric(
                "Confidence",
                f"{confidence:.1f}%"
            )

        except:

            col2.error(
                "Placement prediction failed."
            )

    else:

        score = (
            gpa * 0.30 +
            skills * 0.30 +
            networking * 0.15 +
            internships * 0.15 +
            projects * 0.10
        )

        status = (
            "Placed"
            if score >= 6
            else "Not Placed"
        )

        col2.metric(
            "Placement Prediction",
            status
        )

    # ======================================================
    # CAREER READINESS SCORE
    # ======================================================

    readiness_score = (
        skills * 0.35 +
        networking * 0.25 +
        internships * 0.20 +
        projects * 0.20
    )

    col3.metric(
        "Career Readiness",
        f"{readiness_score:.1f}/10"
    )

    # ======================================================
    # INTERPRETATION
    # ======================================================

    st.subheader(
        "📊 Career Assessment"
    )

    if readiness_score >= 8:

        st.success(
            """
            Excellent profile.
            Strong employability and growth potential.
            """
        )

    elif readiness_score >= 6:

        st.warning(
            """
            Good profile.
            Improve networking and practical experience.
            """
        )

    else:

        st.error(
            """
            Significant skill gaps detected.
            Focus on projects, internships,
            and technical skills.
            """
        )

    # ======================================================
    # CAREER ROADMAP
    # ======================================================

    st.subheader(
        "🛣 Personalized Career Roadmap"
    )

    recommendations = []

    if skills < 6:
        recommendations.append(
            "Improve technical skills through certifications and projects."
        )

    if networking < 6:
        recommendations.append(
            "Participate in networking events and LinkedIn communities."
        )

    if internships < 2:
        recommendations.append(
            "Complete additional internships for practical exposure."
        )

    if projects < 4:
        recommendations.append(
            "Build more real-world portfolio projects."
        )

    if gpa < 7:
        recommendations.append(
            "Strengthen academic performance."
        )

    if len(recommendations) == 0:

        st.success(
            """
            Outstanding profile.
            Continue building leadership and specialization skills.
            """
        )

    else:

        for item in recommendations:

            st.info(item)

    # ======================================================
    # PROFILE SUMMARY
    # ======================================================

    st.subheader(
        "📈 Profile Summary"
    )

    summary_df = pd.DataFrame({
        "Metric": [
            "GPA",
            "Skills",
            "Networking",
            "Internships",
            "Projects"
        ],
        "Score": [
            gpa,
            skills,
            networking,
            internships,
            projects
        ]
    })

    st.dataframe(
        summary_df,
        use_container_width=True
    )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")
st.caption(
    "Career Intelligence Platform • Prediction Engine"
)
