#assignment: survival analysis lab
#Kaplan-Meier Log-Rank Test and Cox proportional hazards regression
#author: Dudleiska Cruz

#imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from lifelines import CoxPHFitter

#kaplan-meier log rank test

km_data = pd.read_csv("km_logrank_readmission.csv")
print("\n--- Kaplan-Meier Dataset ---")
print(km_data.head())

print("\n--- Dataset Information ---")
print(km_data.info())
#check number of patients
print("\n--- Treatment Group Counts ---")
print(km_data["treatment_group"].value_counts())

print("\n--- Missing Values ---")
print(km_data.isnull().sum())

standard_care = km_data[km_data["treatment_group"] == "Standard care"]

telehealth = km_data[km_data["treatment_group"] == "Telehealth follow-up"]

# Create Kaplan-Meier fitter

kmf_standard = KaplanMeierFitter()
kmf_telehealth = KaplanMeierFitter()

kmf_standard.fit(
    durations=standard_care["time_days"],
    event_observed=standard_care["readmitted"],
    label="Standard Care"
)

kmf_telehealth.fit(
    durations=telehealth["time_days"],
    event_observed=telehealth["readmitted"],
    label="Telehealth Follow-up"
)

# Plot Kaplan-Meier survival curves
plt.figure(figsize=(10, 6))

kmf_standard.plot_survival_function()
kmf_telehealth.plot_survival_function()

plt.title("Kaplan-Meier Survival Curve: Hospital Readmission")
plt.xlabel("Days After Hospital Discharge")
plt.ylabel("Probability of Remaining Readmission-Free")
plt.legend()
plt.grid(True)

# Save the figure
plt.savefig("kaplan_meier_survival.png", dpi=300, bbox_inches="tight")

# Display the figure

plt.show()

logrank_results = logrank_test(
    standard_care["time_days"],
    telehealth["time_days"],
    event_observed_A=standard_care["readmitted"],
    event_observed_B=telehealth["readmitted"]
)

# Display log-rank test results

print("\n--- Log-Rank Test Results ---")
print(logrank_results.summary)

#cox proportional hazards analysis
cox_data = pd.read_csv("cox_ph_heart_failure_survival.csv")

# Examine the dataset

print("\n--- Cox Proportional Hazards Dataset ---")
print(cox_data.head())

# Display column names and data types

print("\n--- Dataset Information ---")
cox_data.info()

# Check for missing values

print("\n--- Missing Values ---")
print(cox_data.isnull().sum())

# Display descriptive statistics

print("\n--- Descriptive Statistics ---")
print(cox_data.describe())

#cox proportional hazards model
cox_model_data = cox_data.drop(columns=["patient_id"]).copy()

# Convert categorical variables into numerical variables

cox_model_data = pd.get_dummies(
    cox_model_data,
    columns=["sex"],
    drop_first=True,
    dtype=int
)
# Create the Cox proportional hazards model

cph = CoxPHFitter()

# Fit the Cox proportional hazards model

cph.fit(
    cox_model_data,
    duration_col="time_months",
    event_col="death"
)
# Display the Cox regression results

print("\n--- Cox Proportional Hazards Results ---")
print(cph.summary)

# Create a figure for hazard ratios

plt.figure(figsize=(10, 6))

# Get hazard ratios and confidence intervals

hazard_ratios = cph.hazard_ratios_
confidence_intervals = cph.confidence_intervals_

# Plot hazard ratios
plt.errorbar(
    hazard_ratios,
    hazard_ratios.index,
    xerr=[
        hazard_ratios - np.exp(confidence_intervals.iloc[:, 0]),
        np.exp(confidence_intervals.iloc[:, 1]) - hazard_ratios
    ],
    fmt="o",
    capsize=4
)

# Add reference line at hazard ratio of 1

plt.axvline(x=1, linestyle="--")

# Add titles and labels

plt.title("Cox Proportional Hazards: Heart Failure Survival")
plt.xlabel("Hazard Ratio")
plt.ylabel("Patient Characteristics")

plt.grid(True)

# Save the figure

plt.savefig("cox_proportional_hazards.png", dpi=300, bbox_inches="tight")

# Display the figure

plt.show()

