import pandas as pd

career = pd.read_csv("data/education_career_success.csv")
print(career.columns.tolist())

placement = pd.read_csv("data/placement.csv")
print(placement.columns.tolist())
