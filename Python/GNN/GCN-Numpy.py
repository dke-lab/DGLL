import numpy
import numpy as np
from scipy.linalg import sqrtm
from scipy.special import softmax
import scipy.sparse as sp
import networkx as nx
from networkx.algorithms.community.modularity_max import greedy_modularity_communities
import matplotlib.pyplot as plt
from khop_index import createIndex
from utils.utils import normalize,encode_onehot,Nsubgraph,sparse_mx_to_torch_sparse_tensor

class Khopgraph:
    def __init__(self, Tnode=None, TnodeF=None, label=None, neighborlist=None, neighborFeatures=None, onehop=None, onehopSrc=None, twohop=None, twohopsrc=None, threehop=None, threehopsrc=None):
        self.Tnode = Tnode
        self.label = label
        self.TnodeF = TnodeF
        self.neighborlist = neighborlist
        self.neighborFeaures = neighborFeatures
        self.oneHopNeighbors = onehop
        self.oneHopSrc = onehopSrc
        self.twoHopNeighbors =  twohop
        self.twohopSrc = twohopsrc
        self.threeHopNeighbors = threehop
        self.threehopSrc = threehopsrc

idx_features_labels = np.genfromtxt("{}{}.content".format("./datasets/cora/", "cora"),
                                            dtype=np.dtype(str))
khops = 3;
index = createIndex()

numOfNodes = idx_features_labels.shape[0]
subgraph = Khopgraph()

for x in range(numOfNodes):
    nodeID = idx_features_labels[x, 0]
    lenth = 0
    for ind in index[0]:
        if ind[0] == int(nodeID):
            # subgraph.Tnode = int(nodeID)
            subgraph.Tnode = np.array(int(nodeID))
            # subgraph.TnodeF = idx_features_labels[x,1:1434]
            subgraph.TnodeF = np.array(idx_features_labels[x,1:1434])
            subgraph.label = idx_features_labels[x,1434]
            subgraph.oneHopNeighbors = np.array(ind[1])
            subgraph.oneHopSrc = np.array(subgraph.oneHopNeighbors[:, 0])
            twoHopNeighbors = []
            threeHopNeighbors = []
            if(subgraph.oneHopSrc is not None):
                for node in subgraph.oneHopSrc:
                    for ind1 in index[0]:
                        if ind1[0] == node:
                            twoHopNeighbors.append(np.array(ind1[1]))
                if len(twoHopNeighbors) > 0:
                    subgraph.twoHopNeighbors = np.array(twoHopNeighbors)
                    subgraph.twohopSrc = np.array(subgraph.twoHopNeighbors[:, 0])
            if (subgraph.twohopSrc is not None):
                for node in subgraph.twohopSrc:
                    for ind1 in index[0]:
                        if ind1[0] == node:
                            threeHopNeighbors.append(np.array(ind1[1]))
                if len(threeHopNeighbors) > 0:
                    subgraph.twoHopNeighbors = np.array(threeHopNeighbors)
                    subgraph.threehopSrc = np.array(subgraph.threeHopNeighbors[:, 0])



    #
    #         if(len(subgraph.oneHopNeighbors)>1):
    #             for ind1 in index[1]:
    #                 if ind1[0] == int(nodeID):
    #                     subgraph.twoHopNeighbors = np.array(ind1[1])
    #                     if(len(subgraph.twoHopNeighbors)>1):
    #                         for ind2 in index[2]:
    #                             if ind2[0] == int(nodeID):
    #                                 subgraph.threeHopNeighbors = np.array(ind2[1])
    # if(subgraph.twoHopNeighbors is not None):
    #     subgraph.neighborlist = subgraph.oneHopNeighbors
    #     subgraph.oneHopSrc = np.array(subgraph.oneHopNeighbors[:, 0])
    # elif (subgraph.threeHopNeighbors is not None):
    #     subgraph.neighborlist = subgraph.twoHopNeighbors
    #     subgraph.twohopSrc = np.array(subgraph.twoHopNeighbors[:, 0])
    #     subgraph.twohopSrc = np.intersect1d(subgraph.twohopSrc, subgraph.oneHopSrc)
    # else:
    #     subgraph.neighborlist = subgraph.threeHopNeighbors
    #     if(subgraph.threeHopNeighbors is not None):
    #         subgraph.threehopSrc = np.array(subgraph.threeHopNeighbors[:, 0])
    #         subgraph.threehopSrc = np.intersect1d(subgraph.threehopSrc, subgraph.twohopSrc)
    print(subgraph)
    print("here is subgraph for 3 hops")
    print(f"subgraph TargetNode ID {subgraph.Tnode}")
    print(f"subgraph neighbors {subgraph.neighborlist}")
    print(f"subgraph oneHopNeighbors {subgraph.oneHopNeighbors}")
    print(f"subgraph oneHopSrc {subgraph.oneHopSrc}")
    print(f"subgraph twoHopNeighbors {subgraph.twoHopNeighbors}")
    print(f"subgraph twohopSrc {subgraph.twohopSrc}")
    print(f"subgraph threeHopNeighbors {subgraph.threeHopNeighbors}")
    print(f"subgraph threehopSrc {subgraph.threehopSrc}")
    print("subgraph ends here..")


                # subgraph = Nsubgraph(nodeid=(int(nodeID)), neighborlist=ind[1], nodeFeatures=idx_features_labels[x,1:1434], khop=khops)






