package khop;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;


import Dataset.Node;
import kHop.Util.Util_functions_khop;

public class Khop_Reduce extends MapReduceBase implements Reducer<Text, BytesWritable, Text, BytesWritable> {

	private int minsup;
	private int k;
	int preK = 0;
	private JobConf conf;
	private Path path;
	private Util_functions_khop util;
	File file;

	public void configure(JobConf job) {
	    //minsup = Integer.parseInt(job.get("minsup"));
		path = new Path(job.get("output_writeTofile_path"));
		String kValue = job.get("k");
	    k = Integer.parseInt(kValue);
		
		if(k==1)
			preK =1;
		else
			preK = k-1;
	    this.conf = job;
	    util = new Util_functions_khop();
	    file = util.createFile(path, String.valueOf(k)+"hop.txt");
    }
	@Override
	public void reduce(Text symbol, Iterator<BytesWritable> values, OutputCollector<Text, BytesWritable> output, Reporter reporter) throws IOException {
		// TODO Auto-generated method stub
		try{
			
				System.out.print("reduce starting---for k: " + k);
				System.out.println("key:" + symbol);
				Node_information final_node_inf = null;
				Boolean changed= false;
				Boolean notChanged = true;
				while(values.hasNext())
				{
					
					Node_information node_inf = null;
					BytesWritable value = values.next();
					
					try{
						ByteArrayInputStream byteIn = new ByteArrayInputStream(value.getBytes());
	    				ObjectInputStream in = new ObjectInputStream(byteIn);
	     				
	     				node_inf =(Node_information)in.readObject();
	     				/*System.out.println("---Start Each value:");
	     				node_inf.printInfor();
	     				System.out.println("---End Each value:");*/
	     				in.close();
	     				byteIn.close();	    
	     				if(final_node_inf==null)
	     					final_node_inf = node_inf;
	     				
	     				//if(node_inf.getK_inEdge().get(k)!=null)
	     				changed = inEdge_Merging(final_node_inf, node_inf);
	     				if(changed)
	     					notChanged=false;
	     				//OutEdge_Propagation(output, final_node_inf);
	     				     				
					}
					catch(ClassNotFoundException c)
	  				{
	     				System.out.println(" not found.");
	     				c.printStackTrace();
	  				}	
								
				}
				if(final_node_inf!=null)
				{
					if(!notChanged)
						OutEdge_Propagation(output, final_node_inf);
					else
						System.out.println("do not propagate");
					
					Mapper_Value outValue = new Mapper_Value(final_node_inf);
	 				System.out.println("---Start printing Final each key value:");
	 				System.out.println("ReduceOutKey = '"+symbol+"'");
	 				
	 				
	 				//TODO: write final_node_inf to the text file
	 				
	 				
	 				final_node_inf.printInfor();
	 				
	 				String text = final_node_inf.textToPrint(k)+"\n";
	 				util.writeToFile_append(file, text);
	 				
	 				System.out.println("---End printing Final each key value:");
	 			
	 				output.collect(symbol, outValue.toBytesWritable());	 				
				}

			
		}catch(Exception ex){
			System.out.println("error reduce: "+ex.getMessage());
			ex.printStackTrace(System.out);
			throw ex;
		}
	}
	
	private Boolean inEdge_Merging(Node_information final_node_inf, Node_information node_inf) {

		System.out.print("Merging: ");
		
		Self_Inf self = final_node_inf.getSelf();
		List<Edge_Inf> edgeList_preK1= self.getK_hop().get(preK);
		
		if(self.getK_hop()==null)
			self.setK_hop(new HashMap<Integer, List<Edge_Inf>>());
		
		Self_Inf newSelf = node_inf.getSelf();
		List<Edge_Inf> edgeList_preK2= newSelf.getK_hop().get(preK);
		
		List<Edge_Inf> edgeList_preK3 = new ArrayList();	
		
		addUniqueEdgeList(edgeList_preK3, edgeList_preK1);
		addUniqueEdgeList(edgeList_preK3, edgeList_preK2);
		
		List<Edge_Inf> edgeList_K;
		if(self.getK_hop().get(k)==null)
		{
			edgeList_K= new ArrayList();
			self.getK_hop().put(k,edgeList_K );
		}
		else
		{
			edgeList_K= self.getK_hop().get(k);
		}
		
		int old_edgeSize = edgeList_K.size();
		
		addUniqueEdgeList(edgeList_K,node_inf.getK_inEdge().get(k));
		addUniqueEdgeList(edgeList_K,edgeList_preK3);
		
		List<Edge_Inf> outList= final_node_inf.getOutEdge();
		addUniqueEdgeList(outList,node_inf.getOutEdge());
		final_node_inf.setOutEdge(outList);
		
		
		/*System.out.println("---Start filling khop value:");
		final_node_inf.printInfor();
		System.out.println("---End filling khop value:");*/
		
		if(edgeList_K.size()>old_edgeSize)
			return true;
		else
			return false;
	}
	
	private void addEdgeList(List<Edge_Inf> edgeList, List<Edge_Inf> newList)
	{
		for(Edge_Inf edge: newList)
		{
			if(!edgeList.contains(edge))
			{
				edgeList.add(edge);
			}
		}
	}
	
	private void addUniqueEdgeList(List<Edge_Inf> edgeList, List<Edge_Inf> newList)
	{
		if(newList!=null && edgeList!=null)
		{
			for(Edge_Inf newEdge: newList)
			{
				int count =0;
				int total = edgeList.size();
				for(Edge_Inf edge: edgeList)
				{
					if(newEdge.getNodeA().getId()==edge.getNodeA().getId() && newEdge.getNodeB().getId()==edge.getNodeB().getId())
					{
						break;
					}
					else
						count++;
						
				}
				if(count == total)
					edgeList.add(newEdge);
			}
		}
	}
	
	
	private void OutEdge_Propagation( OutputCollector<Text, BytesWritable> output, Node_information final_node_inf) throws IOException {


		Self_Inf self = final_node_inf.getSelf();
		
		List<Edge_Inf> outEdges = final_node_inf.getOutEdge();
		for(Edge_Inf edge: outEdges)
		{
			Node nodeB = edge.getNodeB();
			Self_Inf self_B = new Self_Inf(nodeB, new ArrayList());
			Map<Integer,List<Edge_Inf>> k_hop= new HashMap<Integer, List<Edge_Inf>>();
			List<Edge_Inf> edge_k_hop = new ArrayList();
			k_hop.put(k, edge_k_hop);
			self_B.setK_hop(k_hop);
				
				
  		    
			String suffix= util.getSuffix(nodeB);
			
			Mapper_Key outKey = new Mapper_Key(nodeB.getId(),suffix);
			
			// Add in_edge at level k for next k-hop.
			Node_information node_inf = new Node_information(self_B,new ArrayList());
			
			Map<Integer, List<Edge_Inf>> k_inEdge = new HashMap<Integer, List<Edge_Inf>>();
			List<Edge_Inf> edgeList = new ArrayList<>();
			edgeList.addAll(self.getK_hop().get(k));
			// Add in_edge at level k for next k-hop for node B
			k_inEdge.put(k+1, edgeList);
			node_inf.setK_inEdge(k_inEdge);
			
			System.out.println("---Start propagation:");
			System.out.println("ReduceOutKey = '"+outKey.toText()+"'");
			node_inf.printInfor();
			System.out.println("---End propagation:");
			Mapper_Value outValue = new Mapper_Value(node_inf);							
			//write output data			
			output.collect(outKey.toText(), outValue.toBytesWritable());
		}
		
		
	}
			

}
