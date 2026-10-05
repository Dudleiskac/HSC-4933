import pandas as pd

df = pd.read_csv("Maternal Health Risk Data Set.csv")

df = df.loc[:,~df.columns.duplicated()]

df.to_excel("Maternal Health Risk Data Set.xlsx", index=False)

print("Dataset successfully converted to XLSX file")
