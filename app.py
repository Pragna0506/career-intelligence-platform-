import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Career Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    padding: 10px;
}

.sub-header {
    font-size: 1.2rem;
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}

.feature-card {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}

.metric-container {
    border-radius: 10px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    try:
        career = pd.read_csv(
            "data/education_career_success.csv"
        )
    except:
        career = pd.DataFrame()

    try:
        placement = pd.read_csv(
            "data/placement.csv"
        )
    except:
        placement = pd.DataFrame()

    return career, placement

career_df, placement_df = load_data()

# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div class="main-header">🚀 Career Intelligence Platform</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-header">AI-Powered Career Analytics, Placement Intelligence, Salary Prediction, and Alumni Tracking</div>',
    unsafe_allow_html=True
)

st.divider()

# =====================================================
# OVERVIEW KPIs
# =====================================================

st.subheader("📊 Platform Overview")

col1, col2, col3, col4 = st.columns(4)

total_students = (
    len(career_df)
    if not career_df.empty
    else 0
)

avg_salary = (
    career_df["Starting_Salary"].mean()
    if (
        not career_df.empty and
        "Starting_Salary" in career_df.columns
    )
    else 0
)

avg_satisfaction = (
    career_df["Career_Satisfaction"].mean()
    if (
        not career_df.empty and
        "Career_Satisfaction" in career_df.columns
    )
    else 0
)

placement_rate = 0

if (
    not placement_df.empty and
    "Placement_Status" in placement_df.columns
):

    placed = (
        placement_df["Placement_Status"]
        .astype(str)
        .str.lower()
        .eq("placed")
        .sum()
    )

    placement_rate = (
        placed / len(placement_df)
    ) * 100

col1.metric(
    "Students",
    f"{total_students:,}"
)

col2.metric(
    "Placement Rate",
    f"{placement_rate:.1f}%"
)

col3.metric(
    "Average Salary",
    f"₹{avg_salary:,.0f}"
)

col4.metric(
    "Career Satisfaction",
    f"{avg_satisfaction:.2f}"
)

st.divider()

# =====================================================
# QUICK INSIGHTS
# =====================================================

st.subheader("📈 Quick Insights")

col1, col2 = st.columns(2)

with col1:

    if (
        not career_df.empty and
        "Starting_Salary" in career_df.columns
    ):

        fig = px.histogram(
            career_df,
            x="Starting_Salary",
            title="Salary Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with col2:

    if (
        not placement_df.empty and
        "Placement_Status" in placement_df.columns
    ):

        fig = px.pie(
            placement_df,
            names="Placement_Status",
            title="Placement Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =====================================================
# PROJECT MODULES
# =====================================================

st.divider()

st.subheader("🎯 Platform Modules")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### 📊 Dashboard
Executive overview of all career analytics.
""")

    st.info("""
### 🎯 Placement Analytics
Placement trends, hiring insights, and outcomes.
""")

    st.info("""
### 📈 Career Analytics
Career growth and success indicators.
""")

    st.info("""
### 💰 Salary Intelligence
Salary trends and compensation analytics.
""")

with col2:

    st.info("""
### 🎯 Skill Gap Analysis
Identify strengths and improvement areas.
""")

    st.info("""
### 🧠 Predictions
Placement and salary prediction engine.
""")

    st.info("""
### 🎓 Alumni Tracker
Track alumni career progression.
""")

    st.info("""
### 🤖 AI Career Advisor
Personalized career recommendations.
""")

# =====================================================
# DATASET PREVIEW
# =====================================================

st.divider()

st.subheader("📋 Dataset Preview")

tab1, tab2 = st.tabs([
    "Career Dataset",
    "Placement Dataset"
])

with tab1:

    if not career_df.empty:
        st.dataframe(
            career_df.head(10),
            use_container_width=True
        )
    else:
        st.warning(
            "education_career_success.csv not found."
        )

with tab2:

    if not placement_df.empty:
        st.dataframe(
            placement_df.head(10),
            use_container_width=True
        )
    else:
        st.warning(
            "placement.csv not found."
        )

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🚀 Career Intelligence")

st.sidebar.success(
    "Use the Pages menu to navigate through the platform."
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
### Available Pages

📊 Dashboard

🎯 Placement Analytics

📈 Career Analytics

💰 Salary Intelligence

🎯 Skill Gap Analysis

🧠 Predictions

🎓 Alumni Tracker

🤖 AI Career Advisor
""")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Career Intelligence Platform | Built with Streamlit, Plotly, Scikit-Learn, and Python"
)
