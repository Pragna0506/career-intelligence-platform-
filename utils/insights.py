import pandas as pd


# =====================================================
# SALARY INSIGHTS
# =====================================================

def get_salary_insights(df):

    insights = []

    if "Starting_Salary" not in df.columns:
        return ["Salary column not found."]

    avg_salary = df["Starting_Salary"].mean()
    max_salary = df["Starting_Salary"].max()
    min_salary = df["Starting_Salary"].min()

    insights.append(
        f"Average salary is ₹{avg_salary:,.0f}"
    )

    insights.append(
        f"Highest salary recorded is ₹{max_salary:,.0f}"
    )

    insights.append(
        f"Lowest salary recorded is ₹
