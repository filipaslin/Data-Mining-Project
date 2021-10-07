import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Read dataset
#df = pd.read_csv("path to DF")
# Try with random data instead
df = pd.DataFrame(np.random.rand(10, 2), columns=['A', 'B'])

# Split to parameters and target i.e. X and y
target = "B"
X, y = df.loc[:, df.columns != target], df[target]
#Split to train and test? 

reg = LinearRegression()

reg.fit(X, y)

# Predict on new data(using all coeeficients)
pred_df = pd.DataFrame(np.arange(5), columns=['A'])
pred = reg.predict(pred_df)

[print("Pred for", i, "=", pred[i]) for i in range(len(pred))]

# Print coefficients found from Linear Regression
coeffs = reg.coef_
intercept = reg.intercept_
print('Coeffs:', coeffs)

# Get the number of coefficients that we want(i.e. beta)
nr = 1
beta = coeffs[:nr]
print('Beta:', beta)

# "Predict" using beta
# Read data to predict. Should be just user attributes, in the same column order as previously to match beta.
#user_attributes = pd.DataFrame()
# Take dot product of user attributes and beta to get predicted susceptibility, use intercept as well maybe?
#B_u = np.dot(beta, user_attributes)