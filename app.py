import streamlit as st
import pandas as pd
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Career Intelligence Platform",
    page_icon="🎓",
    layout="wide"
)

# =========================
# PATH SETUP
# =========================
BASE_DIR = os.path.dirname(__file__)

logo_path = os.path.join(BASE_DIR, "assets", "logo.png")
css_path = os.path.join(BASE_DIR, "assets", "styles.css")
data_path = os.path.join(BASE_DIR, "data3", "education_career_success.csv")

# =========================
# LOAD CSS
# =========================
def load_css():
    try:
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"CSS not loaded: {e}")

load_css()

# =========================
# SIDEBAR LOGO (FIXED)
# =========================
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.warning("Logo not found")

# =========================
# LOAD DATASET
# =========================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

# =========================
# TITLE
# =========================
st.title("🎓 Alumni Career Path Tracker")
st.markdown("### AI Powered Career Analytics Dashboard")

# =========================
# SIDEBAR MENU
# =========================
st.sidebar.title("📌 Navigation")

menu = st.sidebar.radio(
    "Go to",
    ["Home", "Dataset Overview", "Quick Insights"]
)

# =========================
# HOME PAGE
# =========================
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

# =========================
# DATASET PAGE
# =========================
elif menu == "Dataset Overview":
    st.subheader("📊 Dataset Preview")

    if df is not None:
        st.write("Shape:", df.shape)
        st.dataframe(df.head())

# =========================
# INSIGHTS PAGE
# =========================
elif menu == "Quick Insights":
    st.subheader("📈 Quick Insights")

    if df is not None:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Students", df.shape[0])

        with col2:
            if "Starting_Salary" in df.columns:
                st.metric("Avg Salary", round(df["Starting_Salary"].mean(), 2))

        with col3:
            if "Career_Satisfaction" in df.columns:
                st.metric("Avg Satisfaction", round(df["Career_Satisfaction"].mean(), 2))

        st.markdown("---")
        st.dataframe(df.head())

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("🚀 Built with Streamlit | Career Intelligence System")
