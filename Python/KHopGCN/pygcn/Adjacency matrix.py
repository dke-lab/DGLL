import networkx as nx
# coding: utf-8

# In[ ]:


import networkx as nx
G = nx.read_edgelist("virEnvPyDoopPy37/graph.txt", create_using=nx.DiGraph())
G

A = nx.adjacency_matrix(G)
print(A.todense())

