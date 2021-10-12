import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import joblib
import matplotlib.pyplot as plt

##################################################################################################
# Mappers for reducing columns to single variable
def age_mapper(row):
    if row['age_1'] == 1.0:
        return 0
    elif row['age_2'] == 1.0:
        return 1
    elif row['age_3'] == 1.0:
        return 2
    elif row['age_4'] == 1.0:
        return 3
def gender_mapper(row):
    if row['male'] == 1.0:
        return 0
    elif row['female'] == 1.0:
        return 1
def org_mapper(row):
    if row['org_1'] == 1.0:
        return 0
    if row['org_2'] == 1.0:
        return 1

##################################################################################################
# Load datset of user attributes
user_attributes = pd.read_csv("Gossip/users_attribute.txt", sep=" ", header=None, index_col=False)
# Drop index
user_attributes = user_attributes.drop(0, 1)
user_attributes.columns =['verified', 'register_time', 'status_count', 'favourites_count', 'followers_count', 'friend_count', 'male', 'female', 'age_1', 'age_2', 'age_3', 'age_4', 'org_1', 'org_2', 'B']
# Reduce to age, gender and org
user_attributes['gender'] = user_attributes.apply (lambda row: gender_mapper(row), axis=1)
user_attributes['age'] = user_attributes.apply (lambda row: age_mapper(row), axis=1)
user_attributes['org'] = user_attributes.apply (lambda row: org_mapper(row), axis=1)
user_attributes = user_attributes.drop(['age_1', 'age_2', 'age_3', 'age_4', 'male', 'female', 'org_1', 'org_2'], 1)

# Load dataset of user_embeddings. 
# #Change version variable to change version of embedding that is used
version = 0
user_embeddings = ["user_embedding", "user_embedding_t", "user_embedding_ut", "user_embedding_neural"]
user_embedding = np.load("Gossip/" + user_embeddings[version] + ".npy")
user_embedding = pd.DataFrame(user_embedding)

##################################################################################################
# Merge into one dataset
df = user_attributes.copy()
for i in range(user_embedding.shape[1]):
    df['embedding_'+str(i)] = user_embedding.iloc[:, i]

# Split to parameters and target i.e. X and y
target = "B"
X, y = df.loc[:, df.columns != target], df[target]
# Split to train and test? 

#Normalize
X_normalized = preprocessing.normalize(X, axis=0)

##################################################################################################
# Fit Linear Regression to dataset
reg = LinearRegression()
reg.fit(X_normalized, y)
# Get coefficients found from Linear Regression
coeffs = reg.coef_
intercept = reg.intercept_

# Save Linear Regression model for selected user embedding to a file
joblib.dump(reg, 'Models/lin_reg_with_'+user_embeddings[version]+'.pkl') 
# and later you can load it
#reg = joblib.load('filename.pkl')

# Get the number of coefficients that we want(i.e. beta)
nr = len(user_attributes.columns)-1
beta = coeffs[:nr]
print('Beta:', beta)

##################################################################################################
# Plot beta
cols = user_attributes.loc[:, user_attributes.columns != target].columns
plt.bar(cols, beta)
plt.xticks(rotation=45)
plt.show()

##################################################################################################

# "Predict" using beta
# Take dot product of user attributes and beta to get predicted susceptibility, use intercept as well maybe?
#B_u = np.dot(beta, attributes)