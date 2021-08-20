package EdgePartitioning;

import org.apache.hadoop.io.Text;

import fsm.parsemis.graph.SuperNode_GraphId;

public class EdgePartitionMapper_Key{

	public int nodeID;
	public String suffix;
	
	public EdgePartitionMapper_Key(int nodeId, String suffix){
		
		this.nodeID = nodeId;
		this.suffix = suffix;
	}


	public Text toText() {
		Text key = new Text();
		key.set(this.nodeID+this.suffix);
		return key;
	}
}
