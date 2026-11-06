import pandas as pd

maindf = pd.read_csv(
    "eia_coal_consumption_quality_2020_2025.csv",
    dtype={"location": "string", "sector": "string"}
)

# Create a working copy
df = maindf.copy()

# Trim column names
df.columns = df.columns.str.strip()

# Convert text columns to string type and trim whitespace
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
df = df.drop_duplicates().reset_index(drop=True)

# Save cleaned data separately
df.to_csv("coal_cleaned.csv", index=False)

print("Yo chat, I did it!")