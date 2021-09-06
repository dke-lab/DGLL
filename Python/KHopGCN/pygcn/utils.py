import numpy as np
import scipy.sparse as sp
import networkx as nx
import torch
import os
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
# from sklearn.preprocessing import OneHotEncoder

def labelEncoding(classes_list):
    "Generate label encoder for a specific list"
    label_encoder = LabelEncoder()
    label_encoder.fit(classes_list)
    return label_encoder


def oneHotEncoding(integer_encoded):
    "Generate one hot encoding for a specific integer set"
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit(integer_encoded)
    return onehot_encoder


classes_list_str = [

    "Case_Based",
    "Genetic_Algorithms",
    "Neural_Networks",
    "Probabilistic_Methods",
    "Reinforcement_Learning",
    "Rule_Learning",
    "Theory",

]

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

def encode_onehot(labels):
    classes = set(labels)
    classes_dict = {c: np.identity(len(classes))[i, :] for i, c in
                    enumerate(classes)}
    labels_onehot = np.array(list(map(classes_dict.get, labels)),
                             dtype=np.int32)
    return labels_onehot

def generateAdjFeatures(G, idx_features_labels):

    adj = nx.adjacency_matrix(G)
    nodefeatures = np.zeros([G.number_of_nodes(), 1433], dtype=int)
    labels = np.zeros([G.number_of_nodes(), 7], dtype=int)
    i = 0
    for node in G.nodes:
        idx = np.where(idx_features_labels[:, 0][:] == str(node))
        nodefeatures[i] = idx_features_labels[idx, 1:-1]
        labelName = idx_features_labels[idx, -1]
        lblidx = np.where(classes_list_str[:] == labelName[0])
        label_encoder = labelEncoding(classes_list_str)

        # print("classes_list_str[i]", classes_list_str[int(lblidx[0])])
        classes_list_intEncoded = label_encoder.transform(classes_list_str)
        # print("classes_list_intEncoded[i]:", classes_list_intEncoded[int(lblidx[0])])

        onehot_encoder = oneHotEncoding(classes_list_intEncoded)
        onehot_encoder.transform([[classes_list_intEncoded[int(lblidx[0])]]])
        labels[i] = np.array(onehot_encoder.transform([[classes_list_intEncoded[int(lblidx[0])]]]))
        i = i + 1

    # features = normalize(nodefeatures)
    adj = normalize(adj + sp.eye(adj.shape[0]))

    features = torch.FloatTensor(nodefeatures)
    labels = torch.LongTensor(np.where(labels)[1])
    adj = sparse_mx_to_torch_sparse_tensor(adj)
    return adj, features, labels

def load_Khopdata(nodeID=None, neighborlist=None):
    """Load citation network dataset (cora only for now)"""


    idx_features_labels = np.genfromtxt("{}{}.content".format("../data/cora/", "cora"),
                                        dtype=np.dtype(str))


    neighbors = list()
    if os.path.exists("{}{}_3.txt".format("../data/cora/khop/", nodeID)):
        # with FileLock(os.path.expanduser("~/" + "{}.content.lock".format(dataset))):
        G = nx.read_edgelist("{}{}_3.txt".format("../data/cora/khop/", nodeID),create_using=nx.Graph(), nodetype = int)
        for n in G.neighbors(int(nodeID)):
            neighbors.append(n)
        adj, features, labels = generateAdjFeatures(G, idx_features_labels)
    else:
        G = nx.Graph()
        G.add_node(nodeID)
        neighbors.append(nodeID)
        adj, features, labels = generateAdjFeatures(G, idx_features_labels)


    return adj, features, labels, len(neighbors)


def data_load(num_workers = 4):
    new_list = []
    i = 0
    data_list = np.genfromtxt("{}{}.content".format("../data/cora/", "cora"))
    data_list = data_list[:, 0].tolist()
    seg = int(len(data_list) / num_workers)
    while i < len(data_list):
        if (len(data_list) - (i + seg) > seg):
            new_list.append(data_list[i:i + seg])
        else:
            new_list.append(data_list[i:])
        i += seg
    return new_list


def normalize(mx):
    """Row-normalize sparse matrix"""
    rowsum = np.array(mx.sum(1))
    r_inv = np.power(rowsum, -1).flatten()
    r_inv[np.isinf(r_inv)] = 0.
    r_mat_inv = sp.diags(r_inv)
    mx = r_mat_inv.dot(mx)
    return mx


def accuracy(output, labels):
    preds = output.max(1)[1].type_as(labels)
    correct = preds.eq(labels).double()
    correct = correct.sum()
    return correct / len(labels)


def sparse_mx_to_torch_sparse_tensor(sparse_mx):
    """Convert a scipy sparse matrix to a torch sparse tensor."""
    sparse_mx = sparse_mx.tocoo().astype(np.float32)
    indices = torch.from_numpy(
        np.vstack((sparse_mx.row, sparse_mx.col)).astype(np.int64))
    values = torch.from_numpy(sparse_mx.data)
    shape = torch.Size(sparse_mx.shape)
    return torch.sparse.FloatTensor(indices, values, shape)