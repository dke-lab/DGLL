package EdgePartitioning;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.util.List;
import java.util.Map;

import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.MapWritable;
import org.apache.hadoop.io.Text;

import de.parsemis.graph.Node;
import fsm.parsemis.graph.OccurrenceList;
import fsm.parsemis.graph.SuperNode_GraphId;
import khop.Edge_Inf;

public class EdgePartitionMapper_Value {
	List<Edge_Inf> value;


	public EdgePartitionMapper_Value(List<Edge_Inf> edges) {
		this.value = edges;
	}

	public BytesWritable toBytesWritable() {
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		try {
			ObjectOutputStream oos = new ObjectOutputStream(baos);
			oos.writeObject(this.value);
			oos.flush();
			oos.close();
		} catch (IOException e) {
			System.out.println("Mapper at ToByteWritable: exception " + e.getMessage());
			e.printStackTrace();
		}
		return new BytesWritable(baos.toByteArray());
	}
	
	public MapWritable toMapWritable()
	{
		IntWritable sup = new IntWritable(this.value.get(0).getNodeB().getId());
		
		ByteArrayOutputStream baos= new ByteArrayOutputStream();
		try
			{
			
			ObjectOutputStream oos= new ObjectOutputStream(baos);
			oos.writeObject(this.value);
        	oos.flush();
				oos.close();
		}
		catch(IOException e)
			{
				e.printStackTrace();
			}
			
		MapWritable m = new MapWritable();
		m.put(sup,new BytesWritable(baos.toByteArray()));
		
		return m;
	}

}
