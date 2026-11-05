import numpy as np
import pandas as pd

df = pd.read_csv("eia_coal_consumption_quality_2020_2025.csv")

df.head()
df.shape
df.info()
df.describe()
df.isna().sum()