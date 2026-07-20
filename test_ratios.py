from src.dashboard.utils.db import get_ratios

df = get_ratios()

print("\nColumns:")
print(df.columns.tolist())

print("\nUnique Years:")
print(df["year"].unique())

print("\nTotal Rows:")
print(len(df))