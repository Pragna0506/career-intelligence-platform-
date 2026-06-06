import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Placement Analytics",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Placement Analytics Dashboard")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data3/job_placement.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

# ---------------- MAIN ----------------
if df is not None:

    st.subheader("📌 Dataset Overview")
    st.write(df.shape)
    st.dataframe(df.head())

    st.markdown("---")

    # ---------------- METRICS ----------------
    st.subheader("📈 Key Placement Metrics")

    col1, col2, col3 = st.columns(3)

    if "placement_status" in df.columns:

        with col1:
            st.metric("Total Students", df.shape[0])

        with col2:
            placed = df
