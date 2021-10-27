import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn import preprocessing
import joblib
import matplotlib.pyplot as plt

cols = ['user','verified','register_time','status_count','favourites_count','followers_count','friend_count','gender','age','org']
user_attributes = pd.read_csv("Gossip/susceptability_predict.txt", sep=" ", header=None, index_col=False)
user_attributes.columns = cols

#print('User Data')
#print(user_attributes)

users = []
for user in user_attributes['user']:
    users.append(user)
    
#print(users)

user_attributes = user_attributes.drop(['user'], axis=1)

user_attributes = preprocessing.normalize(user_attributes, axis=0)

user_attributes = pd.DataFrame(user_attributes)



model = joblib.load('Models/lin_reg_with_user_embedding_ut.pkl')

beta = model.coef_[:9]
intercept = model.intercept_
#print('\nBeta Coefficients: ')
#print(beta)

#print(beta)
#input()
predict_data = {}

#print('\nSusceptability: ')
for user in range(len(user_attributes)):
    
    user_data = user_attributes.iloc[user].to_numpy()
#    print('Intercept: ', intercept)
    susceptability = intercept
    for i in range(9):
        susceptability += beta[i]*user_data[i]
        #print('Susceptability: ', susceptability)
        #input()
    susceptability = 1 / ( 1 + np.exp(-susceptability))
    #print(susceptability)
    usr = users[user]
    predict_data[usr] = susceptability


keys = predict_data.keys()
values = predict_data.values()

plt.bar(keys,values)
plt.xticks(rotation=60)
plt.subplots_adjust(bottom=0.25)

plt.show()
