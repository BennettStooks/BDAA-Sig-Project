from pathlib import Path 
import pandas as pd 
import statsmodels.api as sm 


csv_path = Path(__file__).resolve().parent / "coal_cleaned.csv"
df = pd.read_csv(csv_path)
# Start of model, this is our demand variable
df.columns = [str(col).strip().lower().replace(" ","-") for col in df.columns]

df = df.replace([float("inf"),float("-inf")],float("nan")).dropna()

Y = df['consumption']
# Collection of our dataset variables 
X = df[['price','heat-content','sulfur-content','ash-content','stocks']]
#Created a intercept with statsmodels for beta_0
X = sm.add_constant(X)
# Now put variables into a OLS model using statsmodes 
model = sm.OLS(Y,X).fit()
#Prints summary 
print(model.summary())