import numpy as np
import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
import torch.optim as optim


import time
import argparse
import math


from gnn.Convolution import GraphSage
from utils.utils import multihop_sampling, load_dataT, accuracy

INPUT_DIM = 1433
HIDDEN_DIM = [128, 7]
NUM_NEIGHBOR_LIST = [10, 10]

assert len(HIDDEN_DIM) == len(NUM_NEIGHBOR_LIST)

BATCH_SIZE = 32
EPOCHS = 20
NUM_BATCH_PER_EPOCH = 20
LEARNING_RATE = 0.01
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


adj, features, labels, idx_train, idx_val, idx_test, adj_table = load_dataT()

model = GraphSage(INPUT_DIM, HIDDEN_DIM, NUM_NEIGHBOR_LIST)

criterion = nn.CrossEntropyLoss().to(DEVICE)
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=5e-4)


def train():
    model.train()
    for e in range(EPOCHS):
        for batch in range(NUM_BATCH_PER_EPOCH):
            batch_src_index = np.random.choice(idx_train, size=(BATCH_SIZE,))
            batch_src_label = torch.from_numpy(labels[batch_src_index]).long().to(DEVICE)
            batch_sampling_result = multihop_sampling(batch_src_index, NUM_NEIGHBOR_LIST, adj_table)
            batch_sampling_x = [torch.from_numpy(features[idx]) for idx in batch_sampling_result]
            batch_train_logits = model(batch_sampling_x)
            loss = criterion(batch_train_logits, batch_src_label)
            optimizer.step()
            loss.backward()
            optimizer.step()
            print("Epoch {:03d} Batch {:03d} Loss: {:.4f}".format(e, batch, loss.item()))


if __name__ == '__main__':
    train()
