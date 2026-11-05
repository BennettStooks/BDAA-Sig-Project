from pathlib import Path 
import pandas as pd 
import statsmodels.api as sm 


# passing our csv through pandas and creating variable
df = pd.read_csv("coal_cleaned.csv")
# Start of model, this is our demand variable
df.columns = [str(col).strip().lower().replace(" ","-") for col in df.columns]

cols = ["consumption","price","heat-content","sulfur-content","ash-content","stocks"]

df = df.replace([float("inf"),float("-inf")],float("nan")).dropna()

Y = df['consumption']
# Collection of our dataset variables 
X = df[['price','heat-conent','sulfur-content','ash-content','stocks']]
#Created a intercept with statsmodels for beta_0
X = sm.add_constant(X)
# Now put variables into a OLS model using statsmodes 
model = sm.OLS(Y,X).fit()
#Prints summary 
print(model.summary())