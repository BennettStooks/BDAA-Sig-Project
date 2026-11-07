
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from pathlib import Path

#Loading cleaned dataset
base_dir = Path(__file__).resolve().parent
df = pd.read_csv(base_dir / "coal_cleaned.csv")

#Keep state-level observations only
#Exclude U.S. and regional totals to avoid duplication
state_codes = set("""
AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA
ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH
OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC
""".split())

df = df[df["location_code"].isin(state_codes)].copy()

#Focus on Electric Utility (sector 1)
df = df[df["sector"] == 1].copy()

#Remove invalid and missing model observations
predictors = [
    "price", "heat-content",
    "sulfur-content", "ash-content"
]

model_df = df.dropna(
    subset=["consumption"] + predictors
).copy()

model_df = model_df[
    (model_df["consumption"] > 0) &
    (model_df["price"] > 0) &
    (model_df["heat-content"] > 0)
].copy()

#Log transform consumption
model_df["log_consumption"] = np.log(
    model_df["consumption"]
)

#Fitting OLS with state and year controls
formula = (
    'log_consumption ~ price'
    ' + Q("heat-content")'
    ' + Q("sulfur-content")'
    ' + Q("ash-content")'
    ' + C(location_code)'
    ' + C(period)'
)

model = smf.ols(
    formula,
    data=model_df
).fit(cov_type="HC3")

#Displaying results
print(model.summary())
print("Observations:", int(model.nobs))
print("R-squared:", round(model.rsquared, 4))

# Saving regression summary
with open(base_dir / "ols_results.txt", "w") as f:
    f.write(model.summary().as_text())

#Export model results for Tableau
tableau_df = model_df.loc[model.fittedvalues.index].copy()

tableau_df["actual_log_consumption"] = (tableau_df["log_consumption"])

tableau_df["predicted_log_consumption"] = (
    model.fittedvalues
)
tableau_df["residual"] = model.resid

#Adjusted Price vs Consumptions
controls = (
    'Q("heat-content")'
    ' + Q("sulfur-content")'
    ' + Q("ash-content")'
    ' + C(location_code)'
    ' + C(period)'
)

adjusted_y = smf.ols(
    "log_consumption ~ " + controls,
    data=tableau_df
).fit()

adjusted_x = smf.ols(
    "price ~ " + controls,
    data=tableau_df
).fit()

tableau_df["adjusted_consumption"] = (
    adjusted_y.resid
)

tableau_df["adjusted_price"] = (
    adjusted_x.resid
)

# Save observations for Tableau graphs 8, 9, 10
tableau_df.to_csv(
    base_dir / "tableau_ols_observations.csv",
    index=False
)


#Coefficients and Confidence Intervals
variables = {
    "price": "Coal Price",
    'Q("heat-content")': "Heat Content",
    'Q("sulfur-content")': "Sulfur Content",
    'Q("ash-content")': "Ash Content"
}

results = []

for variable, label in variables.items():

    beta = model.params[variable]
    lower, upper = model.conf_int().loc[variable]

    # Express the effect for a 1-SD increase
    # so predictors are more comparable.
    original_column = (
        variable.replace('Q("', '').replace('")', '')
    )
    sd = tableau_df[original_column].std()

    results.append({
        "Variable": label,
        "Coefficient": beta,
        "P_value": model.pvalues[variable],
        "Standardized_effect": beta * sd,
        "Lower_CI": lower * sd,
        "Upper_CI": upper * sd,
    })

coef_df = pd.DataFrame(results)

coef_df.to_csv(
    base_dir / "tableau_ols_coefficients.csv",
    index=False
)

print("Tableau export files created successfully!")