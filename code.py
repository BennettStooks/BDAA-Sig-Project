import pandas as pd

maindf = pd.read_csv(
    "eia_coal_consumption_quality_2020_2025.csv",
    dtype={"location": "string", "sector": "string"}
)

# Create a working copy for cleaning
df = maindf.copy()

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Convert text columns to string type and trim spaces
text_columns = df.select_dtypes(include=["object", "string"]).columns

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Convert blank cells to missing values
df = df.replace(r"^\s*$", pd.NA, regex=True)

# Clarify location column names
df = df.rename(columns={
    "location": "location_code",
    "stateDescription": "location_name"
})

# Remove exact duplicate rows
rows_before = len(df)
df = df.drop_duplicates().reset_index(drop=True)

print("Duplicate rows removed:", rows_before - len(df))
print("Original shape:", maindf.shape)
print("Cleaned shape:", df.shape)

# Review missing values
print("\nMissing values per column:")
print(df.isna().sum())

missing_columns = df.columns[df.isna().any()]

missing_by_sector = (
    df.groupby("sectorDescription")[missing_columns]
    .agg(lambda column: column.isna().mean() * 100)
    .round(1)
)

print("\nMissing values by sector (%):")
print(missing_by_sector.to_string())

# Check for negative measurements
measurement_columns = [
    "ash-content",
    "consumption",
    "heat-content",
    "price",
    "receipts",
    "stocks",
    "sulfur-content"
]

negative_mask = (df[measurement_columns] < 0).any(axis=1)

print("\nNegative values per column:")
print((df[measurement_columns] < 0).sum())

if negative_mask.any():
    print("\nRows containing negative measurements:")
    print(df.loc[negative_mask].to_string())

# Check for repeated year/location/sector combinations
key_columns = ["period", "location_code", "sector"]
repeated_keys = df.duplicated(subset=key_columns, keep=False)

print("\nRows with repeated year/location/sector:")
print(repeated_keys.sum())

# Review heat-content scales
print("\nHeat content by year and sector:")
print(
    df.groupby(["period", "sectorDescription"])["heat-content"]
    .agg(["count", "min", "median", "max"])
    .to_string()
)

# Preserve missing values and zeros.
# Keep all geographic and sector levels in this master dataset.
# Heat-content and volume units still need verification.
# Do not convert their values or overwrite unit labels yet.

# Save after all cleaning steps
df.to_csv("coal_cleaned.csv", index=False)

print("\nCleaned file saved!")