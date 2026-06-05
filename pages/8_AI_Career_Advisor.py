import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Career Advisor",
    page_icon="🤖",
    layout="wide"
)

# ==========================================================
# TITLE
# ==========================================================

st.title("🤖 AI Career Advisor")

st.markdown("""
Get personalized career guidance, skill recommendations,
placement readiness insights, and salary improvement suggestions.
""")

st.divider()

# ==========================================================
# USER PROFILE INPUT
# ==========================================================

st.subheader("👨‍🎓 Student Profile")

col1, col2 = st.columns(2)

with col1:

    gpa = st.slider(
        "University GPA",
        0.0,
        10.0,
        7.0
    )

    skills = st.slider(
        "Technical Skills Score",
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
        5
    )

    certifications = st.slider(
        "Certifications Completed",
        0,
        20,
        2
    )

# ==========================================================
# CAREER READINESS SCORE
# ==========================================================

career_score = (
    skills * 0.30 +
    networking * 0.20 +
    internships * 0.20 +
    projects * 0.15 +
    certifications * 0.15
)

# ==========================================================
# SCORE DISPLAY
# ==========================================================

st.subheader("📊 Career Readiness Score")

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=career_score,
        title={"text": "Career Readiness"},
        gauge={
            "axis": {"range": [0, 10]}
        }
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# CAREER CATEGORY
# ==========================================================

if career_score >= 8:
    category = "High Potential"
elif career_score >= 6:
    category = "Career Ready"
else:
    category = "Needs Improvement"

st.success(
    f"Career Category: {category}"
)

st.divider()

# ==========================================================
# AI RECOMMENDATIONS
# ==========================================================

st.subheader("🧠 AI Career Recommendations")

recommendations = []

if gpa < 7:
    recommendations.append(
        "Improve academic performance to strengthen your profile."
    )

if skills < 6:
    recommendations.append(
        "Focus on Python, SQL, Data Analytics, Machine Learning, and Cloud technologies."
    )

if networking < 6:
    recommendations.append(
        "Attend industry events, conferences, hackathons, and grow your LinkedIn network."
    )

if internships < 2:
    recommendations.append(
        "Complete additional internships to gain practical industry experience."
    )

if projects < 5:
    recommendations.append(
        "Build more real-world projects and publish them on GitHub."
    )

if certifications < 3:
    recommendations.append(
        "Earn certifications from Coursera, Google, AWS, Microsoft, or IBM."
    )

if len(recommendations) == 0:
    recommendations.append(
        "Excellent profile. Focus on leadership, innovation, and specialization."
    )

for rec in recommendations:
    st.info(rec)

# ==========================================================
# CAREER ROADMAP
# ==========================================================

st.subheader("🛣 Personalized Career Roadmap")

roadmap = []

if skills < 5:
    roadmap.append(
        "Step 1: Strengthen programming fundamentals."
    )

if projects < 5:
    roadmap.append(
        "Step 2: Build portfolio projects."
    )

if internships < 2:
    roadmap.append(
        "Step 3: Complete internships."
    )

if networking < 6:
    roadmap.append(
        "Step 4: Expand professional network."
    )

roadmap.append(
    "Step 5: Prepare for placements and interviews."
)

roadmap.append(
    "Step 6: Continue learning advanced technologies."
)

for step in roadmap:
    st.write(step)

# ==========================================================
# SALARY POTENTIAL
# ==========================================================

st.subheader("💰 Estimated Salary Potential")

salary_score = (
    gpa * 0.20 +
    skills * 0.30 +
    internships * 0.20 +
    projects * 0.15 +
    networking * 0.15
)

estimated_salary = (
    salary_score * 100000
)

st.metric(
    "Estimated Starting Salary",
    f"₹{estimated_salary:,.0f}"
)

# ==========================================================
# PLACEMENT READINESS
# ==========================================================

st.subheader("🎯 Placement Readiness")

placement_score = (
    gpa * 0.30 +
    skills * 0.30 +
    internships * 0.20 +
    networking * 0.20
)

placement_probability = min(
    placement_score * 10,
    100
)

st.progress(
    int(placement_probability)
)

st.write(
    f"Placement Probability: {placement_probability:.1f}%"
)

# ==========================================================
# TOP CAREER PATHS
# ==========================================================

st.subheader("🚀 Recommended Career Paths")

career_paths = []

if skills >= 8:

    career_paths.extend([
        "Data Scientist",
        "Machine Learning Engineer",
        "AI Engineer"
    ])

elif skills >= 6:

    career_paths.extend([
        "Data Analyst",
        "Business Analyst",
        "Software Developer"
    ])

else:

    career_paths.extend([
        "Junior Analyst",
        "Technical Support Engineer",
        "Graduate Trainee"
    ])

for path in career_paths:
    st.success(path)

# ==========================================================
# SKILL GAP ANALYSIS
# ==========================================================

st.subheader("📈 Skill Gap Analysis")

gap_df = pd.DataFrame({
    "Area": [
        "Technical Skills",
        "Networking",
        "Projects",
        "Internships",
        "Certifications"
    ],
    "Current Score": [
        skills,
        networking,
        min(projects, 10),
        internships,
        min(certifications, 10)
    ],
    "Target Score": [
        8,
        8,
        8,
        4,
        5
    ]
})

st.dataframe(
    gap_df,
    use_container_width=True
)

# ==========================================================
# LEARNING RESOURCES
# ==========================================================

st.subheader("📚 Suggested Learning Resources")

resources = [
    "Python for Data Science",
    "SQL for Analytics",
    "Machine Learning Fundamentals",
    "Power BI / Tableau",
    "AWS Cloud Practitioner",
    "Git & GitHub",
    "Data Structures and Algorithms",
    "Interview Preparation"
]

for item in resources:
    st.write(f"✅ {item}")

# ==========================================================
# ACTION PLAN
# ==========================================================

st.subheader("📋 90-Day Action Plan")

plan = pd.DataFrame({
    "Month": [
        "Month 1",
        "Month 2",
        "Month 3"
    ],
    "Goal": [
        "Improve Technical Skills",
        "Build Projects",
        "Placement Preparation"
    ]
})

st.dataframe(
    plan,
    use_container_width=True
)

# ==========================================================
# EXPORT REPORT
# ==========================================================

st.subheader("📥 Download Career Report")

report = pd.DataFrame({
    "Metric": [
        "Career Readiness",
        "Placement Probability",
        "Estimated Salary"
    ],
    "Value": [
        round(career_score, 2),
        round(placement_probability, 2),
        round(estimated_salary, 2)
    ]
})

csv = report.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Career Report",
    data=csv,
    file_name="career_advisor_report.csv",
    mime="text/csv"
)

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")
st.caption(
    "Career Intelligence Platform • AI Career Advisor"
)
