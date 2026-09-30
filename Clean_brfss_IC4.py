import pandas as pd
import numpy as np

df = pd.read_csv("eye_health_behavioral_risk_factors_dataset_2022_brfss.csv")
print(df.shape,
      df.dtypes,
      df.isnull().sum(),
      df.nunique(),
      sep="\n")

print("Duplicates:", df.duplicated().sum())

df = df.dropna(axis=1, how="all")
df=df.drop(columns= [c for c in df.columns if c.endswith("ID")])

df = df.dropna(subset=["Data_Value"])
df = df.drop(columns=["Geolocation","Data_Value_Footnote","StateAbbr","NonWeightedSample","Geographic Level", "Numerator"])

df.columns = df.columns.str.lower().str.replace(" ","_")
df["error"] = (df["high_confidence_limit"] - df["low_confidence_limit"]) /2
df["prevalence_level"] = np.select([df["data_value"] <5,df["data_value"] <= 7 ],["low","medium"],"high")

df.to_csv("eye_health_2022_clean.csv", index=False)

print(pd.read_csv("eye_health_2022_clean.csv").shape == df.shape)
print(pd.read_csv("eye_health_2022_clean.csv").shape)
print(pd.read_csv("eye_health_2022_clean.csv").head)







