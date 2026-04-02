# check_dataset.py
import pandas as pd

df = pd.read_csv("dataset_merged.csv")
print("Columns:", df.columns.tolist())
print(df.head(5))
