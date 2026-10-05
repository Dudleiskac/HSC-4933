import pandas as pd

df = pd.read_csv("Maternal Health Risk Data Set.csv")

df = df.loc[:,~df.columns.duplicated()]

df.to_json("Maternal Health Risk Data Set.parquet", orient="records", indent=4)

print("Dataset successfully converted to JSON file")
