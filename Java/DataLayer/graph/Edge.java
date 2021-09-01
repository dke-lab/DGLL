package datalayer.graph;

import java.util.HashMap;

public class Edge {
    private long src;
    private long dst;
    private final HashMap<String, Object> properties;

    public Edge() {
        properties = new HashMap<>();
    }

    public Edge(long src, long dst) {
        this();
        this.src = src;
        this.dst = dst;
    }

    public Edge(long src, long dst, HashMap<String, Object> properties) {
        this.src = src;
        this.dst = dst;
        this.properties = properties;
    }

    public long getSource() {
        return this.src;
    }

    public long getDestination() {
        return this.dst;
    }

    public void setSource(long src) {
        this.src = src;
    }

    public void setDestination(long dst) {
        this.dst = dst;
    }

    public HashMap<String, ?> getProperties() {
        return this.properties;
    }

    public <T> T getProperty(String key) {
        return (T) properties.get(key);
    }

    public <T> void setProperty(String key, T value) {
        properties.put(key, value);
    }
}
