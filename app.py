import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="Career Intelligence Platform",
    page_icon="🎓",
    layout="wide"
)

# Title
st.title("🎓 Alumni Career Path Tracker")
st.markdown("### AI Powered Career Analytics Dashboard")

# Load dataset safely
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data3/education_career_success.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

# Sidebar menu
st.sidebar.title("📌 Navigation")

menu = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Dataset Overview",
        "Quick Insights"
    ]
)

# ---------------- HOME ----------------
if menu == "Home":
    st.subheader("🏠 Welcome")

    st.write("""
    This platform helps analyze:
    - Student career growth
    - Placement prediction trends
    - Salary intelligence
    - Skill gap analysis
    - Alumni career tracking
    """)

    st.success("Use sidebar to explore different modules")

# ---------------- DATASET ----------------
elif menu == "Dataset Overview":
    st.subheader("📊 Dataset Preview")

    if df is not None:
        st.write("Shape:", df.shape)
        st.dataframe(df.head())

# ---------------- INSIGHTS ----------------
elif menu == "Quick Insights":
    st.subheader("📈 Quick Insights")

    if df is not None:

        st.write("### Key Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Students", df.shape[0])

        with col2:
            if "Starting_Salary" in df.columns:
                st.metric("Avg Salary", round(df["Starting_Salary"].mean(), 2))

        with col3:
            if "Career_Satisfaction" in df.columns:
                st.metric("Avg Satisfaction", round(df["Career_Satisfaction"].mean(), 2))

        st.write("---")

        st.write("### Data Preview")
        st.dataframe(df.head())

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("🚀 Built with Streamlit | Career Intelligence System")
