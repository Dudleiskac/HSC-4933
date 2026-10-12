#scatterplots and OLS regression
#Writer:Dudleiska Cruz

#This script will create scatterplots,calcuate, snd OLS regression line, and save plots when the user requests it

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import re


def to_snake_case(column_name):
    "convert column names to lowercase snake_case"
    name = str(column_name).strip()
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"[^A-Za-z0-9]+", "_", name)
    return name.strip("_").lower()
#ask user for dataset
dataset_path = input("Enter the dataset filename: ")
df = pd.read_csv(dataset_path)

#clean the column name
df.columns = [to_snake_case(column) for column in df.columns]
print("Available column names:", df.columns.tolist())
for column in df.columns:
    print(column)

#Ask user to select the x and y variables

x_col = input("\nEnter the X (independent) variable name: ").strip().lower()
y_col = input("Enter the Y (dependent) variable name: ").strip().lower()

if x_col not in df.columns or y_col not in df.cloumns:
    print("one or both column names were not found.")
else:
    data = df[[x_col,y_col]].copy()

    data[x_col] = pd.to_numeric(data[x_col], errors="coerce")
    data[y_col] = pd.to_numeric(data[y_col], errors="coerce")
    data = data.dropna(subset=[x_col,y_col])

    print("Rows remaining after removing the missing values:", len(data))
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(
        data[x_col],data[y_col],
        alpha=0.6, edgecolor="black", linewidth=0.3
)
ax.set_xlabel(x_col)
ax.set_ylabel(y_col)
ax.set_title(f"{y_col} vs {x_col} (n = {len(data)})")
ax.grid(alpha=0.3)
fig.tight_layout()

#save scatterplot
save_plot = input("\nWould you like to save this scatterplot? (yes/no): ").strip().lower()
if save_plot == "yes":
    filename = input("Enter a filename (example:scatterplot.png): ")
    if not filename.endswith(".png"):
        filename += ".png"
    fig.savefig(filename, dpi=300)
    print("scatterplot saved as:", filename)
plt.show()
plt.close(fig)

#calcuate the OLS regression
x = sm.add_constant(data[x_col])
model = sm.OLS(data[y_col], x).fit()

#show regression results
print("\nOLS Regression Results:")
print(model.summary())

print("Intercept (beta 0):", model.params["const"])
print("Slope (beta 1):", model.params[x_col])
print("R-squared:", model.rsquared)

x_line = np.linespace(data[x_col].min(), data[x_col].max(),100)
y_line = (model.params["const"]+model.params[x_col]*x_line)
#plot scatterplot with OLS regression line
fig, ax = plt.subplots(figsize=(8,6))
ax.scatter(data[x_col],data[y_col], alpha=0.6, edgecolor="black", linewidth=0.3,label="observed data")
ax.plot(x_line, y_line, color="crimson", linewidth=2, label=f"OLS Line (R²={model.rsquared: .3f})")
ax.set_xlabel(x_col)
ax.set_ylabel(y_col)
ax.set_title(f"{y_col} vs {x_col} with OLS Regression Line")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()

#ask user to save the OLS scatterplot
save_ols = input("\nWould you like to save this scatterplot with OLS regression line? (yes/no): ").strip().lower()
if save_ols == "yes":
    ols_filename = input("Enter a filename (example: regression.png): ").strip()
    if not ols_filename.endswith(".png"): ols_filename += ".png"
    fig.savefig(ols_filename, dpi=300)
    print("OLS scatterplot saved as:", ols_filename)
plt.show()
plt.close(fig)






