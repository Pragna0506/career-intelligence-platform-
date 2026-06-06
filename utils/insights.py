import pandas as pd

def generate_insights(df):
    insights = []

    insights.append(f"Total Records: {df.shape[0]}")
    insights.append(f"Total Features: {df.shape[1]}")

    if "Starting_Salary" in df.columns:
        insights.append(f"Average Salary: {df['Starting_Salary'].mean():,.2f}")

    if "University_GPA" in df.columns:
        insights.append(f"Average GPA: {df['University_GPA'].mean():.2f}")

    if "Career_Satisfaction" in df.columns:
        insights.append(f"Average Career Satisfaction: {df['Career_Satisfaction'].mean():.2f}")

    if "Gender" in df.columns:
        top_gender = df["Gender"].mode()[0]
        insights.append(f"Most Common Gender: {top_gender}")

    return insights


def top_correlation(df):
    numeric_df = df.select_dtypes(include=["int64", "float64"])
    corr = numeric_df.corr()
    return corr
