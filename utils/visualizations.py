import matplotlib.pyplot as plt
import seaborn as sns

def plot_distribution(df, column):
    plt.figure(figsize=(6,4))
    sns.histplot(df[column], kde=True)
    plt.title(f"Distribution of {column}")
    plt.show()


def plot_count(df, column):
    plt.figure(figsize=(6,4))
    sns.countplot(x=df[column])
    plt.title(f"Count of {column}")
    plt.xticks(rotation=45)
    plt.show()


def plot_correlation_heatmap(df):
    plt.figure(figsize=(10,6))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.show()
