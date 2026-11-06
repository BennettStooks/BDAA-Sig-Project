
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf


# 1. Load cleaned dataset
base_dir = Path(__file__).resolve().parent
df = pd.read_csv(base_dir / "coal_cleaned.csv")

# 2. Keep state-level observations only
# Exclude U.S. and regional totals to avoid duplication
state_codes = set("""
AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA
ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH
OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC
""".split())

df = df[df["location_code"].isin(state_codes)].copy()

# 3. Focus on Electric Utility (sector 1)
df = df[df["sector"] == 1].copy()

# 4. Remove invalid and missing model observations
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

# 5. Log transform consumption
model_df["log_consumption"] = np.log(
    model_df["consumption"]
)

# 6. Fit OLS with state and year controls
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

# 7. Display results
print(model.summary())
print("Observations:", int(model.nobs))
print("R-squared:", round(model.rsquared, 4))

# 8. Save regression summary
with open(base_dir / "ols_results.txt", "w") as f:
    f.write(model.summary().as_text())


