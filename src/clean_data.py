import pandas as pd
from pathlib import Path

data_dir = Path(__file__).resolve().parent.parent / "data"

maindf = pd.read_csv(
    data_dir / "eia_coal_consumption_quality_2020_2025.csv",
    dtype={"location": "string", "sector": "string"},
)
# Create a working copy
df = maindf.copy()

# Inspect Data:
df.head()
df.info()

# Clean Column names and text

df.columns = df.columns.str.strip() # Trim column names

# Convert text to string type and trim whitespace
text_columns = df.select_dtypes(
    include=["object", "string"]) 

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Standardize missing values:
df = df.replace(r"^\s*$", pd.NA, regex=True) 


# Clarify location column names
df = df.rename(columns={
    "location": "location_code",
    "stateDescription": "location_name"
})

# Remove duplicate rows
df = df.drop_duplicates().reset_index(drop=True)

# Review Units
#Review Units
measurement_columns = [
    "ash-content",
    "consumption",
    "heat-content",
    "price",
    "receipts",
    "stocks",
    "sulfur-content",
]

print("\nUNITS BY MEASUREMENT")

for column in measurement_columns:
    unit_column = f"{column}-units"
    units = df[unit_column].dropna().unique().tolist()
    print(f"{column}: {units}")

# Compare heat-content scales across sectors
print("\nHEAT CONTENT BY SECTOR AND UNIT")

print(
    df.groupby(
        ["sectorDescription", "heat-content-units"],
        dropna=False,
    )["heat-content"]
    .agg(["count", "min", "median", "max"])
    .to_string()
)

# Review Potential Outliers
state_codes = set("""
AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA
ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH
OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC
""".split())

state_df = df.loc[
    df["location_code"].isin(state_codes)
].copy()

print("\nPOTENTIAL OUTLIERS")

for column in measurement_columns:
    # Compare observations within the same sector and unit
    grouped = state_df.groupby(
        ["sectorDescription", f"{column}-units"],
        dropna=False,
    )[column]

    q1 = grouped.transform("quantile", q=0.25)
    q3 = grouped.transform("quantile", q=0.75)
    iqr = q3 - q1

    # Flag values outside 1.5 times the interquartile range.
    # Skip groups with no spread between the quartiles.
    outlier_mask = (
        (state_df[column] < q1 - 1.5 * iqr)
        | (state_df[column] > q3 + 1.5 * iqr)
    ) & (iqr > 0)

    print(f"\n{column}: {int(outlier_mask.sum())} potential outliers")

    if outlier_mask.any():
        print("First 10 flagged records:")
        print(
            state_df.loc[
                outlier_mask,
                ["period", "location_name", "sectorDescription", column],
            ]
            .head(10)
            .to_string(index=False)
        )


# Save cleaned data separately
df.to_csv(data_dir / "coal_cleaned.csv", index=False)
