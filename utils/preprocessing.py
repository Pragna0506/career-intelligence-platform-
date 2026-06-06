import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_data(df):
    df = df.copy()

    # remove duplicates
    df = df.drop_duplicates()

    # fill missing values
    for col in df.columns:
        if df[col].dtype == "object":
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].mean(), inplace=True)

    return df


def encode_categorical(df, categorical_cols):
    df = df.copy()
    encoders = {}

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    return df, encoders
