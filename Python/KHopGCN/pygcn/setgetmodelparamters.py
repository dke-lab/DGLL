import torch
def getWeights(self):
    return {k: v.cpu() for k, v in self.state_dict().items()}


def setWeights(self, weights):
    self.load_state_dict(weights)


def getGradients(self):
    grads = []
    for p in self.parameters():
        grad = None if p.grad is None else p.grad.data.cpu().numpy()
        grads.append(grad)
    return grads


def setGradients(self, gradients):
    for g, p in zip(gradients, self.parameters()):
        if g is not None:
            p.grad = torch.from_numpy(g)