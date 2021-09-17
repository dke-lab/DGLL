package dgll.datalayer.mapper;

import dgll.datalayer.graph.Edge;
import dgll.datalayer.graph.Graph;
import dgll.datalayer.graph.Node;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Csv {
    public static Graph importCsv(List<String> data, Boolean header) {
        Graph graph = new Graph();

        int start = 0;
        if (header) start++;

        Map<Long, Long> map = new HashMap<>();

        for (int i = start; i < data.size(); i++) {
            String[] arr = data.get(i).split(",");

            long src = Long.parseLong(arr[0].replaceAll("^\"|\"$", ""));
            long dst = Long.parseLong(arr[1].replaceAll("^\"|\"$", ""));

            if (!map.containsKey(src)) map.put(src, src);
            if (!map.containsKey(dst)) map.put(dst, dst);

            graph.addEdge(new Edge(src, dst));
        }

        for (Long key : map.keySet()) {
            graph.addNode(new Node(key));
        }

        return graph;
    }
}
