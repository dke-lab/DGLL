package datalayer.graph;

import java.util.HashMap;

public class Node {
    private long id;
    private final HashMap<String, Object> properties;

    public Node() {
        properties = new HashMap<>();
    }

    public Node(long id) {
        this();
        this.id = id;
    }

    public Node(long id, HashMap<String, Object> properties) {
        this.id = id;
        this.properties = properties;
    }

    public long getId() {
        return this.id;
    }

    public void setId(long id) {
        this.id = id;
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
