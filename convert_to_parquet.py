import pandas as pd

df = pd.read_csv("Maternal Health Risk Data Set.csv")

df = df.loc[:,~df.columns.duplicated()]

df.to_parquet("Maternal Health Risk Data Set.parquet", index=False)

print("Dataset successfully converted to parquet file")
