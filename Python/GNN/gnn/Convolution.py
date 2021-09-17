import numpy as np
import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
import math


class NeighborAggregator(nn.Module):
    def __init__(self, input_dim, output_dim, use_bias=False, aggr_method="mean"):
        super(NeighborAggregator, self).__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.use_bias = use_bias
        self.aggr_method = aggr_method
        self.weight = nn.Parameter(torch.Tensor(self.input_dim, self.output_dim))

        if use_bias:
            self.bias = nn.Parameter(torch.Tensor(self.output_dim))

        self.reset_parameters()

    def reset_parameters(self):
        init.kaiming_uniform_(self.weight)
        if self.use_bias:
            init.zeros_(self.bias)

    def forward(self, neighbor_feature):
        if self.aggr_method == "mean":
            neighbor_feature.mean(dim=1)
        elif self.aggr_method == "sum":
            neighbor_feature.sum(dim=1)
        elif self.aggr_method == "max":
            neighbor_feature.max(dim=1)
        else:
            raise ValueError("Unsupported aggr_method, expected mean, sum, max, but got {}".format(self.aggr_method))
        neighbor_hidden = torch.matmul(neighbor_feature, self.weight)
        if self.use_bias:
            neighbor_hidden += self.bias

        return neighbor_hidden


class SageGCN(nn.Module):
    def __init__(self, input_dim, hidden_dim,
                 activation=F.relu,
                 aggr_neighbor_method="mean",
                 aggr_hid_method="sum"):

        super(SageGCN, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.activation = activation
        self.aggr_hid_method = aggr_hid_method
        self.aggr_neighbor_method = aggr_neighbor_method

        self.weight = nn.Parameter(torch.Tensor(self.input_dim, self.hidden_dim))

        self.neighborAgg = NeighborAggregator(self.input_dim, self.hidden_dim, aggr_method=aggr_neighbor_method)

    def reset_parameters(self):
        init.kaiming_uniform_(self.weight)

    def forward(self, src_node_features, neighbor_node_features):
        neighbor_hidden = self.neighborAgg(neighbor_node_features)
        self_hidden = torch.matmul(src_node_features, self.weight)

        if self.aggr_hid_method == "sum":
            hidden = self_hidden + neighbor_hidden
        elif self.aggr_hid_method == "concat":
            hidden = torch.cat([self_hidden, neighbor_hidden], dim=1)
        else:
            raise ValueError("Expected sum or concat, got {}".format(self.aggr_hid_method))

        if self.activation:
            hidden = self.activation(hidden)
        return hidden


class GraphSage(nn.Module, object):
    """docstring for GraphSage"""

    def __init__(self, input_dim, hidden_dim=[64, 64], num_neighbors_list=[10, 10]):
        super(GraphSage, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_neighbors_list = num_neighbors_list

        self.gcn = []
        self.gcn1 = SageGCN(input_dim, hidden_dim[0])
        self.gcn2 = SageGCN(hidden_dim[0], hidden_dim[1])
        self.gcn.append(self.gcn1)
        self.gcn.append(self.gcn2)

        self.num_layers = len(num_neighbors_list)

    def forward(self, node_feature_list):
        hidden = node_feature_list
        for l in range(self.num_layers):
            next_hidden = []
            gcn = self.gcn[l]
            for hop in range(self.num_layers - l):
                src_nodes = hidden[hop]
                src_nums = len(src_nodes)
                h = gcn(src_nodes, hidden[hop + 1].view(src_nums, self.num_neighbors_list[l], -1))
                next_hidden.append(h)
            hidden = next_hidden
        return hidden[0]


class GraphConvolution(nn.Module):

    def __init__(self, in_features, out_features, bias=True):
        super(GraphConvolution, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = nn.Parameter(torch.FloatTensor(in_features, out_features))
        if bias:
            self.bias = nn.Parameter(torch.FloatTensor(out_features))
        else:
            self.register_parameter('bias', None)

        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1. / math.sqrt(self.weight.size(1))
        self.weight.data.uniform_(-stdv, stdv)
        if self.bias is not None:
            self.bias.data.uniform_(-stdv, stdv)

    def forward(self, x, adj):
        support = torch.mm(x, self.weight) # matrix multiplication
        output = torch.spmm(adj, support)  # sparse matrix multiplication
        if self.bias is not None:
            return output + self.bias
        else:
            return output

    def __repr__(self):
        return self.__class__.__name__ + ' (' \
               + str(self.in_features) + ' -> ' \
               + str(self.out_features) + ')'


class GCN(nn.Module):
    def __init__(self, in_features, nhid, nclass, dropout):
        super(GCN, self).__init__()
        self.in_features = in_features
        self.nhid = nhid
        self.nclass = nclass
        self.dropout = dropout
        self.gcn1 = GraphConvolution(in_features, nhid)
        self.gcn2 = GraphConvolution(nhid, nclass)

    def forward(self, x, adj):
        h1 = F.relu(self.gcn1(x, adj))
        h1_d = F.dropout(h1, self.dropout, training=self.training)
        logits = self.gcn2(h1_d, adj)
        output = F.log_softmax(logits, dim=1)
        return output