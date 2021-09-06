import ray
from pygcn.model import GCN
from pygcn.utils import load_Khopdata
import torch.nn.functional as F

@ray.remote
class DataWorker(object):
    def __init__(self, dropout, data_loader):
        self.model = GCN(nfeat=1433,
            nhid=32,
            nclass=7,
            dropout=dropout)
        self.data_loader = data_loader
        self.data_iterator = iter(self.data_loader)

    def compute_gradients(self, weights):
        self.model.set_weights(weights)
        try:
            # data, target = next(self.data_iterator)

            for self.nodeID in next(self.data_iterator):
            # self.nodeID = next(self.data_iterator)
            #     print("Loading Khop Data of the node:", int(self.nodeID))
                adj, features, labels, neighborNumber = load_Khopdata(int(self.nodeID), -1)
        except StopIteration:  # When the epoch ends, start a new epoch.
            self.data_iterator = iter(self.data_loader)
            self.nodeID = next(self.data_iterator)
            adj, features, labels, neighborNumber = load_Khopdata(self.nodeID, -1)
        self.model.zero_grad()
        output = self.model(features, adj)
        loss = F.nll_loss(output, labels)
        loss.backward()
        return self.model.get_gradients()