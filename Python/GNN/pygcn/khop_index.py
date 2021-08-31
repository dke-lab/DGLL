index = []

for file in ["hop1", "hop2", "hop3"]:
    with open(file) as f:
        edges = [edge.rstrip() for edge in f]
    arr = []
    for edge in edges:
        arr2 = []
        arr3 = []
        x = edge.split(',')
        y = x[1].split(' ')
        arr2.append(int(x[0]))
        for e in y:
            z = e.split('-')
            arr4 = [int(z[0]), int(z[1])]
            arr3.append(arr4)
        arr2.append(arr3)
        arr.append(arr2)

    index.append(arr)

def get(hop, node):
    for x in index[hop]:
        if x[0] == node:
            return x[1]

subgraph = get(2, 128)
print(subgraph)
