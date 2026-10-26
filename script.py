"""
Author: Dudleiska Cruz
Lab 8: Logistic and count-variable regression
HSC 4933 - Python for Health Analytics

This scripts loads a data set, cleans column names, allows users to
select predictors and a response variable, and runs regression models.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from statsmodels.stats.outliers_influence import variance_inflation_factor

def clean_column_name(column_name):
    """Convert a column name to lowercase snake_case."""
    import re

    name = str(column_name).strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")

def load_dataset():
    """ Ask the user for a csv file and load the dataset."""

    file_path = input("Enter the path to your CSV dataset:").strip()
    df = pd.read_csv(file_path)

    #clean the colum names
    df.columns = [clean_column_name(column) for column in df.columns]

    #display datset information
    print("\nDataset loaded successfully!")
    print(f"Number of rows: {df.shape[0]}")
    print(f"Number of columns:{df.shape[1]}")

    #list all available columns
    print("\nAvailable column names:")
    for column in df.columns:
        print(column)
    return df

def select_columns(df):
    """ask user to select predictors and a response variable."""
    print("\nAvailable columns")
    for column in df.columns:
        print(column)
    #ask for the response variable
    response = input(
        "\nEnter the response variable column name:"

    ).strip()
    if response not in df.columns:
        raise ValueError("The response column was not found.")

    predictors_input = input(
        "Enter predictor column names seperated by commas"
    )

    predictors = [
        column.strip()
        for column in predictors_input.split(",")
        if column.strip()
    ]
    #validate the selected predictors

    if not predictors:
        raise ValueError("You must select at least one predictor.")
    if len(predictors) != len(set(predictors)):
        raise ValueError("you selected a predictor more than once.")
    for column in predictors:
        if column not in df.columns:
            raise ValueError(
                f"predictor column '{column}' was not found."

            )
    print ("\nSelected predictors:", predictors)
    print("selected response:", response)

    return predictors, response
def prepare_data(df, predictors, response):
    """ prepare selected columns for regression."""

    #keep only the selected predictors and response
    selected_data = df[predictors + [response]].copy()

    for column in selected_data.columns:
        selected_data[column] = pd.to_numeric(
            selected_data[column], errors="coerce"

        )
    selected_data = selected_data.replace(
        [np.inf], np.nan
    )

    selected_data = selected_data.dropna()
    if selected_data.empty:
        raise ValueError(
            "No complete numeric rows remain after cleaning."
        )

    x = selected_data[predictors]
    y = selected_data[response]

    print("\nData preparation complete!")
    print(f"Rows remaining:{len(selected_data)}")
    print(f"predictors columns: {len(predictors)}")
    print(f"response column: {response}")

    return x, y

def run_logistic_regression(x,y):
    """Run the logistic regression model results."""

    if not set(y.unique()).issubset({0,1}) or y.nunique() != 2:
        raise ValueError(
            "the response variable must contain both 0 and 1."

        )
    for column in x.columns:
        if not set(x[column].unique()).issubset({0,1}):
            raise ValueError(
                f"predictor '{column}' must contain only 0 and 1."
            )
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)

    accuracy = accuracy_score(y_test, predictions)

    report = classification_report(
        y_test, predictions, zero_division=0
    )

    matrix = confusion_matrix(
        y_test, predictions, labels=[0,1]


    )
    #calculate pseudo-R-squared
    x_constant = sm.add_constant(x, has_constant="add")
    logit_model = sm.Logit(y, x_constant).fit(disp=False)
    pseudo_rsquared = logit_model.prsquared
    print("\nLOGISTIC REGRESSION RESULTS")
    print("---------------------------")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"McFadden pseudo-R-squared: {pseudo_rsquared:.4f}")
    print("\nClassification Report:")
    print(report)
    print("Confusion Matrix (actual rows, predicted columns):")
    print(matrix)

    return model, accuracy, report, matrix

def run_poisson_regression(X, y):
    """Run Poisson regression and calculate VIF values."""

    # Poisson regression requires non-negative response values
    if (y < 0).any():
        raise ValueError(
            "The response variable cannot contain negative values."
        )
    X_constant = sm.add_constant(X, has_constant="add")

    # Fit the Poisson regression model
    model = sm.GLM(
        y,
        X_constant,
        family=sm.families.Poisson()
    ).fit()
    vif_results = []

    for index, column in enumerate(X.columns, start=1):
        vif_value = variance_inflation_factor(
            X_constant.to_numpy(), index
        )

        vif_results.append((column, vif_value))
    print("\nPOISSON REGRESSION RESULTS")
    print("--------------------------")
    print(model.summary())

    print("\nPseudo-R-squared:")
    print(f"{model.pseudo_rsquared():.4f}")

    print("\nVariance Inflation Factors (VIF):")
    for column, vif_value in vif_results:
        print(f"{column}: {vif_value:.4f}")
    print("\nSignificant predictors (p < 0.05):")
    significant = model.pvalues[
        (model.pvalues < 0.05) &
        (model.pvalues.index != "const")
    ]
    if significant.empty:
        print("No significant predictors found.")
    else:
        for column in significant.index:
            print(
                f"{column}: coefficient = {model.params[column]:.6f}, "
                f"p-value = {model.pvalues[column]:.6g}"
            )

    return model, vif_results

def save_output(output_text):
    """Ask the user whether to save results to a text file."""

    choice = input(
        "\nWould you like to save the output to a .txt file? (y/n): "
    ).strip().lower()

    if choice in ("y", "yes"):
        filename = input(
            "Enter a name for the output file: "
        ).strip()
        if not filename:
            print("No filename entered. Output was not saved.")
            return

            # Ensure the filename ends in .txt
        if not filename.lower().endswith(".txt"):
            filename += ".txt"

            # Save the output
        with open(filename, "w", encoding="utf-8") as file:
            file.write(output_text)

        print(f"\nOutput saved successfully as {filename}")
    else:
        print("\nOutput was not saved.")
def main():
    """Run the complete regression program."""

    # Load the dataset
    df = load_dataset()

    # Select predictors and response
    predictors, response = select_columns(df)

    # Prepare the selected data
    X, y = prepare_data(df, predictors, response)

    # Ask which regression model to run
    regression_type = input(
        "\nChoose regression type (logistic or poisson): "
    ).strip().lower()

    # Capture the regression output as text
    import io
    from contextlib import redirect_stdout

    output_buffer = io.StringIO()

    with redirect_stdout(output_buffer):
        if regression_type == "logistic":
            run_logistic_regression(X, y)

        elif regression_type == "poisson":
            run_poisson_regression(X, y)

        else:
            raise ValueError(
                "Invalid choice. Enter 'logistic' or 'poisson'."
            )

    # Display the captured results
    output_text = output_buffer.getvalue()
    print("\n" + output_text)

    # Ask whether to save the output
    save_output(output_text)


if __name__ == "__main__":
    main()
