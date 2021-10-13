"""
Codes for preprocessing real-world datasets and computing propensity scores used in the experiments
"""
import codecs
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import sparse, stats
from sklearn.model_selection import train_test_split
import networkx as nx
import matplotlib.pyplot as plt
import os, time, pickle, progressbar


path = os.getcwd() + '/'
plotdir = path + 'Plots/'
if not os.path.isdir(plotdir):
    os.makedirs(os.path.dirname(plotdir))

# Biased Sampling
SubSample = 2500
writetofile = 1

starttime = time.time()

print('Load: \'all_users_attribute.pkl\'')
f = open(path + "Data/all_users_attribute.pkl","rb")
users=pickle.load(f)
f.close()

edges_list=[]
news_list=[]
news_list_true = []
edges_list_true = []

print('Load: \'gossipcop_content_no_ignore.tsv\'')
news=pd.read_csv(path + 'Data/dEFEND data(5)/dEFEND data/gossipcop_content_no_ignore.tsv', sep='\t', header=0)
print('News: ')
print(news.head())
news=news.set_index('id').T.to_dict('list')


# Progress Bar
print('Step 1 / 8')
bar = progressbar.ProgressBar(maxval=len(users.keys()), widgets=[progressbar.Bar('=','[',']'),' ', progressbar.Percentage()])
bar.start()

index_bar = 0

index_iteration = 0


for item in users.keys():
    if SubSample == 0 or index_bar < SubSample:
        # Increment
        index_bar += 1
        bar.update(index_bar)
        ####################
        user_news=users[item]['news_ids']    
        for new_id in user_news:
            if new_id not in news.keys():
                continue
            elif news[new_id][0]==1:
                news_list.append(new_id)
                edges_list.append((item,new_id))
            elif news[new_id][0]==0:
                news_list_true.append(new_id)
                edges_list_true.append((item,new_id))
    else: pass

bar.finish()

print('Fake: ')
print(len(news_list))
print(len(edges_list))
print('True: ')
print(len(news_list_true))
print(len(edges_list_true))

news_list=list(dict.fromkeys(news_list))
B=nx.Graph()
B.add_nodes_from(users.keys(),bipartite=0)
B.add_nodes_from(news_list,bipartite=1)
B.add_edges_from(edges_list)

#print(B.number_of_edges())
B.remove_nodes_from(list(nx.isolates(B)))
#print(B.number_of_nodes())
#print(nx.is_connected(B))



if writetofile:
    filename = 'plot_1.graphml'
    print('Write plot to file: \'', filename, '\'')
    nx.write_graphml(B,plotdir + filename)


B_real=nx.Graph()
B_real.add_nodes_from(users.keys(),bipartite=0)
B_real.add_nodes_from(news_list_true,bipartite=1)
B_real.add_edges_from(edges_list_true)

B_real.remove_nodes_from(list(nx.isolates(B_real)))

if writetofile:
    filename = 'plot_true_data.graphml'
    print('Write plot to file: \'', filename, '\'')
    nx.write_graphml(B_real,plotdir + filename)



B_full = nx.Graph()
B_full.add_nodes_from(users.keys(),nodetype=0)
B_full.add_nodes_from(news_list_true,nodetype=1)
B_full.add_nodes_from(news_list,nodetype=2)
B_full.add_edges_from(edges_list_true, edgetype=0)
B_full.add_edges_from(edges_list, edgetype=1)

B_full.remove_nodes_from(list(nx.isolates(B_full)))

if writetofile:
    filename = 'full.graphml'
    print('Write plot to file: \'', filename, '\'')
    nx.write_graphml(B_full,plotdir + filename)

print('Statistics: ')


print(B_full)
full_dict = dict(B_full.nodes(data=True))

final = {}

for key in full_dict:
    if full_dict[key]['nodetype'] == 0:
        try:
            r = B_real.degree[key]
        except: r = 0
        try: 
            f = B.degree[key]
        except: f = 0
        if r + f > 0:
            s = f / (f+r)
        else: s = 0
        print(key,' - Fake: ', f, ' - Real: ', r, ' Susceptability: ', s)
    

'''
"""Load and Preprocess datasets."""
# load dataset.
col = {0: 'user', 1: 'item'}
with open(f'Data/Gossip/train-pscore.txt', 'r') as f:
    data_train = pd.read_csv(f, delimiter=' ', header=None)
    data_train.rename(columns=col, inplace=True)
with open(f'Data/Gossip/test-pscore.txt', 'r') as f:
    data_test = pd.read_csv(f, delimiter=' ', header=None)
    data_test.rename(columns=col, inplace=True)
'''


   
#vertices = range(1, 10)
#edges = [(7,2), (2,3), (7,4), (4,5), (7,3), (1,6), (1,7), (2,8), (2,9)]

#G = nx.Graph()
#G.add_nodes_from(vertices)
#G.add_edges_from(edges)

#nx.draw(G)

#plt.savefig("Plots/ExampleGraph.png")
