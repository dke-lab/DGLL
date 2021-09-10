import ray
from pygcn.model import GCN
import torch
import numpy as np
@ray.remote
class ParameterServer(object):
    def __init__(self, lr, dropout):
        self.model = GCN(nfeat=1433,
            nhid=32,
            nclass=7,
            dropout=dropout)
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=lr)

    def apply_gradients(self, *gradients):
        summed_gradients = [
            np.stack(gradient_zip).sum(axis=0)
            for gradient_zip in zip(*gradients)
        ]
        self.optimizer.zero_grad()
        self.model.set_gradients(summed_gradients)
        self.optimizer.step()
        return self.model.get_weights()

    def get_weights(self):
        return self.model.get_weights()