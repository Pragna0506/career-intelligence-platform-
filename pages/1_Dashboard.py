import pandas as pd

career = pd.read_csv("data3/education_career_success.csv")
print(career.columns.tolist())

placement = pd.read_csv("data3/job_placement.csv")
print(placement.columns.tolist())
