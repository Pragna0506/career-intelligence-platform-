import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Career Intelligence Dashboard")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data3/education_career_success.csv")
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
    st.subheader("📈 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", df.shape[0])

    with col2:
        if "Starting_Salary" in df.columns:
            st.metric("Avg Salary", round(df["Starting_Salary"].mean(), 2))

    with col3:
        if "University_GPA" in df.columns:
            st.metric("Avg GPA", round(df["University_GPA"].mean(), 2))

    with col4:
        if "Career_Satisfaction" in df.columns:
            st.metric("Avg Satisfaction", round(df["Career_Satisfaction"].mean(), 2))

    st.markdown("---")

    # ---------------- CHARTS ----------------
    st.subheader("📊 Visual Analytics")

    # 1. Salary Distribution
    if "Starting_Salary" in df.columns:
        fig1 = px.histogram(df, x="Starting_Salary", nbins=30, title="Salary Distribution")
        st.plotly_chart(fig1, use_container_width=True)

    # 2. GPA vs Salary
    if "University_GPA" in df.columns and "Starting_Salary" in df.columns:
        fig2 = px.scatter(
            df,
            x="University_GPA",
            y="Starting_Salary",
            color="Gender" if "Gender" in df.columns else None,
            title="GPA vs Salary"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 3. FIXED: Field of Study Distribution
    if "Field_of_Study" in df.columns:

        field_counts = df["Field_of_Study"].value_counts().reset_index()
        field_counts.columns = ["Field_of_Study", "Count"]

        fig3 = px.bar(
            field_counts,
            x="Field_of_Study",
            y="Count",
            title="Field of Study Distribution"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # 4. Career Satisfaction
    if "Career_Satisfaction" in df.columns:
        fig4 = px.histogram(
            df,
            x="Career_Satisfaction",
            nbins=20,
            title="Career Satisfaction Distribution"
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # ---------------- INSIGHTS ----------------
    st.subheader("💡 Key Insights")

    if "Starting_Salary" in df.columns:
        st.write("✔ Average Salary:", round(df["Starting_Salary"].mean(), 2))

    if "University_GPA" in df.columns:
        st.write("✔ Average GPA:", round(df["University_GPA"].mean(), 2))

    if "Career_Satisfaction" in df.columns:
        st.write("✔ Average Satisfaction:", round(df["Career_Satisfaction"].mean(), 2))

    if "Field_of_Study" in df.columns:
        st.write("✔ Most Common Field:", df["Field_of_Study"].mode()[0])

else:
    st.error("Dataset not found. Please check file path.")

# Footer
st.markdown("---")
st.markdown("🚀 Career Intelligence Platform | Dashboard Module")
