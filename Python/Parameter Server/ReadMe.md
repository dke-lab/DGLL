# Parameter Server¶ and Data Workers
The parameter server is a framework for distributed machine learning training. In the parameter server framework, 
a centralized server tains global shared parameters of a machine-learning model  while 
the data and computation of calculating updates (i.e., gradient descent updates) are distributed over worker nodes.


# Requirement
- Python 3.6.9+
- PyTorch 1.9.0+cu102
- Ray v1.6.0

# How to utilize the code

```
    learning_rate = 1e-2
    dropout = 0.5
    data_loader = load_data(data)
    num_workers = 4
    ray.init(ignore_reinit_error=True)
    ps = ParameterServer.remote(learning_rate, dropout)
    workers = [DataWorker.remote(dropout, data_loader) for i in range(num_workers)]
    current_weights = ps.get_weights.remote()
    gradients = [
            worker.compute_gradients.remote(current_weights) for worker in workers
        ]
        current_weights = ps.apply_gradients.remote(*gradients)
```

Provided for academic use only

