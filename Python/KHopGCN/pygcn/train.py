from __future__ import division
from __future__ import print_function

import time
import argparse
import numpy as np

import torch
import torch.nn.functional as F
import torch.optim as optim
from numpy import random
from pygcn.utils import load_Khopdata, accuracy, data_load
from pygcn.khop_index import createIndex
from pygcn.model import GCN
from pygcn.parameterserver import ParameterServer
from pygcn.dataworker import DataWorker
import ray



def main_GCN():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='Disables CUDA training.')
    parser.add_argument('--fastmode', action='store_true', default=False,
                        help='Validate during training pass.')
    parser.add_argument('--seed', type=int, default=42, help='Random seed.')
    parser.add_argument('--epochs', type=int, default=200,
                        help='Number of epochs to train.')
    parser.add_argument('--lr', type=float, default=0.01,
                        help='Initial learning rate.')
    parser.add_argument('--weight_decay', type=float, default=5e-4,
                        help='Weight decay (L2 loss on parameters).')
    parser.add_argument('--hidden', type=int, default=16,
                        help='Number of hidden units.')
    parser.add_argument('--dropout', type=float, default=0.5,
                        help='Dropout rate (1 - keep probability).')
    parser.add_argument('--workers', type=int, default=4,
                        help='number of workers.')

    args = parser.parse_args()
    train(args)


def train(args):
    args.cuda = not args.no_cuda and torch.cuda.is_available()

    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.cuda:
        torch.cuda.manual_seed(args.seed)
    model = GCN(nfeat=1433,
                nhid=32,
                nclass=7,
                dropout=args.dropout)

    data_loader =  data_load(num_workers = args.workers)
    ray.init(ignore_reinit_error=True)
    ps = ParameterServer.remote(1e-2, args.dropout)
    workers = [DataWorker.remote(args.dropout, data_loader) for i in range(args.workers)]
    print("Running parameter server training.")
    current_weights = ps.get_weights.remote()
    for i in range(args.epochs):
        print("iter:", i + 1)
        model.train()
        gradients = [
            worker.compute_gradients.remote(current_weights) for worker in workers
        ]
        # Calculate update after all gradients are available.
        current_weights = ps.apply_gradients.remote(*gradients)

        if i % 1 == 0:
            model.eval()
            # Evaluate the current model.
            model.set_weights(ray.get(current_weights))
            node_list = list()
            data_iterator = data_loader
            node_list = [item for sublist in list(data_iterator) for item in sublist]
            for testnodeID in node_list:
                adj, features, labels, _ = load_Khopdata(int(testnodeID), -1)
                outputs = model(features, adj)
                acc_train = accuracy(outputs, labels)
                print('acc_train: {:.4f}'.format(acc_train.item()))
    ray.shutdown()
main_GCN()