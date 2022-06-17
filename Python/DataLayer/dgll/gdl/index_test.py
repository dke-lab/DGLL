from dgll.gdl.index.subgraph_index import SubgraphIndex
from dgll.gdl.index.vertex_index import VertexIndex

vertex_index = VertexIndex()
subgraph_index = SubgraphIndex()

attributes = [1,2,3]
vertex_index.insert(1, attributes)
node = vertex_index.get(vertex_id=1)
print(node)
subgraph = [[1,2],[2,3]]
subgraph_index.insert(vertex_id=1, data=subgraph)
node = subgraph_index.get(vertex_id=1)
print(node)


