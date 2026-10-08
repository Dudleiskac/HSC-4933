#clinical decison making.    #
#####


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

#environment variables
CSV_PATH = "Blood_Pressure_clean.csv"
X_COL = "sys_mmhg"
Y_COL = "dias_mmhg"

df = pd.read_csv(CSV_PATH)
data = df[[X_COL, Y_COL]].dropna()

fig,ax = plt.subplots(figsize=(8,6))
ax.scatter(data[X_COL], data[Y_COL], alpha=0.6, edgecolor="k", linewidth=0.3)
ax.set_xlabel(X_COL)
ax.set_ylabel(Y_COL)
ax.set_title(f"{Y_COL} vs {X_COL} (n = {len(data)})")
ax.grid(alpha=0.3)
fig.tight_layout()

scatter_file = f"{X_COL}_vs_{Y_COL}_scatter.png"
fig.savefig(scatter_file, dpi=300)
print("Saved scatterplot -> {scatter_file}")

X = sm.add_constant(data[X_COL])
model = sm.OLS(data[Y_COL], X).fit()

print("OLS Regression Summary:")
print(model.summary())
#make new scatterplot with regresssion line

x_line = np.linspace(data[X_COL].min(), data[X_COL].max(),num=100)
y_line = model.params["const"] + model.params[X_COL] * x_line
ax.plot(x_line, y_line, color="crimson", linewidth=2, label=f"OLS Line(R² = {model.rsquared:3f}")
ax.set_title(f"{Y_COL} vs {X_COL} with OLS Line (n = {len(data)})")
ax.legend()

#save new scatterplot

Ols_file = f"{X_COL}_vs_{Y_COL}_ols.png"
fig.savefig(Ols_file, dpi=300)
print(f"saved scatterplot with OLS file -> {Ols_file}")

#display OLS regression
plt.show()




