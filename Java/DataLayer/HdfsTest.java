import dgll.datalayer.graph.Graph;
import dgll.datalayer.mapper.Csv;
import dgll.datalayer.storage.Hdfs;

import java.io.IOException;
import java.time.Duration;
import java.time.Instant;

public class HdfsTest {
    public static void main(String[] args) throws IOException {
        Hdfs hdfs = new Hdfs("URL");
        Graph graph = Csv.importCsv(hdfs.read("/tmp/cora.csv"), true);
        System.out.println(graph.nodeCount());
        System.out.println(graph.edgeCount());
    }
}
