import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Select Models
versions = [0,1,3]

class ModelStorage():
    def __init__(self, version):
        user_embeddings = ["user_embedding_na","user_embedding", "user_embedding_t", "user_embedding_ut", "user_embedding_neural"]
        path = 'Models/lin_reg_with_'+user_embeddings[version]
        self.model = joblib.load(path + '.pkl')
        self.data = pd.read_pickle(path + '_DATA.pd')

        self.target = self.data['B']
        self.user_attributes = self.data.drop('B', axis=1)

        self.cols = self.user_attributes.columns    
        self.beta = self.model.coef_[:9]

        self.coef_ = self.model.coef_
        self.intercept = self.model.intercept_
        self.name = user_embeddings[version]

models = []
for version in versions:
    models.append(ModelStorage(version))
cols = []
for col in models[0].cols:
    cols.append(col)

fig, ax = plt.subplots()
width = 0.2
i = 0
rects = []
for model in models:
    rects.append(ax.bar(np.arange(len(model.cols)) + i*width, model.beta, width = width, label=model.name))
    i += 1

ax.set_xticks(np.arange(len(models[0].cols)))
ax.set_xticklabels(cols)
ax.legend()
fig.tight_layout()
plt.xticks(rotation=45)
plt.subplots_adjust(bottom=0.25)

plt.show()
