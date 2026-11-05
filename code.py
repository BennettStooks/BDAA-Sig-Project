import numpy as np
import pandas as pd

maindf = pd.read_csv("eia_coal_consumption_quality_2020_2025.csv")

# Create a working copy for cleaning
df = maindf.copy()

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Remove extra spaces around text values
for column in df.select_dtypes(include="object").columns:
    df[column] = df[column].str.strip()

# Convert blank cells to missing values
df = df.replace(r"^\s*$", pd.NA, regex=True)

# Remove exact duplicate rows
rows_before = len(df)
df = df.drop_duplicates().reset_index(drop=True)
print("Duplicate rows removed:", rows_before - len(df))

# Review missing values
print("\nMissing values:")
print(df.isna().sum())

# Save the cleaned data
df.to_csv("coal_cleaned.csv", index=False)

# Convert text columns from object to pandas string type
text_columns = df.select_dtypes(include="object").columns
df[text_columns] = df[text_columns].astype("string")

# Sector numbers are category codes, not measurements
df["sector"] = df["sector"].astype("string")

# Check the updated types
print("\nUpdated data types:")
print(df.dtypes)

print("\nCleaned file saved!") 