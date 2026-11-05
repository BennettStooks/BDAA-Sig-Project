import pandas as pd
import statsmodels.api as sm
from pathlib import Path

base_dir = Path(__file__).resolve().parent
csv_path = base_dir / "coal_cleaned.csv"

if not csv_path.exists():
    raise FileNotFoundError(
        f"CSV file not found: {csv_path}. "
        "Make sure 'coal_cleaned.csv' is in the same folder as this script."
    )

df = pd.read_csv(csv_path)
print("Loaded CSV:", csv_path)
print("Columns:", list(df.columns))

# Normalize the CSV header names to match the actual dataset format
# (lowercase and hyphenated, such as 'heat-content' and 'sulfur-content')
df.columns = [str(col).strip().lower().replace(" ", "-") for col in df.columns]

required_columns = [
    "consumption",
    "price",
    "heat-content",
    "sulfur-content",
    "ash-content",
    "stocks",
]

missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(
        f"Missing required column(s): {missing_columns}. "
        "Check the exact names in your CSV file."
    )

# Keep only the variables used in the regression and remove NaN/inf rows
model_df = (
    df[required_columns]
    .copy()
    .replace([float("inf"), float("-inf")], float("nan"))
    .dropna()
)

Y = model_df["consumption"]
X = model_df[["price", "heat-content", "sulfur-content", "ash-content", "stocks"]]
X = sm.add_constant(X)

model = sm.OLS(Y, X).fit()
print(model.summary())
