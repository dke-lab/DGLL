package datalayer.graph;

import java.util.ArrayList;
import java.util.List;

public class Graph {
    private List<Node> nodes;
    private List<Edge> edges;

    public Graph() {
        nodes = new ArrayList<>();
        edges = new ArrayList<>();
    }

    public Graph(List<Node> nodes) {
        this();
        this.nodes = nodes;
    }

    public Graph(List<Node> nodes, List<Edge> edges) {
        this.nodes = nodes;
        this.edges = edges;
    }

    public void addNode(Node node) {
        this.nodes.add(node);
    }

    public void removeNode(long nodeId) {
        this.nodes.removeIf(node -> node.getId() == nodeId);
    }

    public void AddEdge(Edge edge) {
        this.edges.add(edge);
    }

    public void removeEdge(long src, long dst) {
        this.edges.removeIf(edge -> edge.getSource() == src && edge.getDestination() == dst);
    }
}
