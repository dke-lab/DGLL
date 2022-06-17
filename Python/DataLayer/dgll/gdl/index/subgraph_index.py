from dgll.gdl.index.index import Index


class SubgraphIndex(Index):
    def __init__(self):
        Index.__init__(self, "subgraph")