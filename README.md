# Data-Mining-Project
Project in course Data Mining.

Parts of the data and the code are taken from: https://github.com/GitHubLuCheng/Causal-Understanding-of-Fake-News-Dissemination

Folder "Gossip" contains the data.

Run user_attribute.py and create_bipartite.py to run preprocessing of data.

The files BPRMF.py, BPRMF_t.py, BPRMF_ut.py and BPRMF_neural.py reads from the preprocessed data and outputs user embeddings.

The file model_train.py trains a Linear Regression and writes the model to a file in the folder "Models".

The file plot_models.py plots the coefficients from the models in the folder "Models".
