import numpy as np
from scipy.linalg import sqrtm
from scipy.special import softmax
import networkx as nx
from networkx.algorithms.community.modularity_max import greedy_modularity_communities
import matplotlib.pyplot as plt
from matplotlib import animation
# matplotlib inline
from IPython.display import HTML
A = np.array(
    [[0, 1, 0, 0, 0], [1, 0, 1, 0, 0], [0, 1, 0, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]]
)
A
feats = np.arange(A.shape[0]).reshape((-1,1))+1
feats
H = A @ feats
H

D = np.zeros(A.shape)
np.fill_diagonal(D, A.sum(axis=0))
D
D_inv = np.linalg.inv(D)
D_inv
D_inv @ A

H_avg = D_inv @ A @ feats
H_avg
g = nx.from_numpy_array(A)
A_mod = A + np.eye(g.number_of_nodes())
# D for A_mod:
D_mod = np.zeros_like(A_mod)
np.fill_diagonal(D_mod, A_mod.sum(axis=1).flatten())

# Inverse square root of D:
D_mod_invroot = np.linalg.inv(sqrtm(D_mod))
D_mod
