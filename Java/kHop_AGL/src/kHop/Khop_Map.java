package khop;
import java.util.*;
import java.util.Map.Entry;
import java.io.*;
import java.lang.*;
import java.text.ParseException;

import kHop.Util.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.*;
import org.apache.hadoop.util.ToolRunner;

import Dataset.Node;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;


public class Khop_Map extends MapReduceBase implements Mapper<NullWritable, Text, Text, BytesWritable>	{

	private JobConf conf;
	private int k;
	@Override
	public void configure(JobConf conf)
	{
		this.conf = conf;
		String kValue = conf.get("k");
	    k = Integer.parseInt(kValue);

	}
	
	/**
	 * key:
	 * value: path to similar supernode table file
	 * outputKey: a pair of (graphId,SuperNode_Labels) !?
	 * outputValue: list of "(graphId, SuperNode_Labels)" !?
	 */
	
	@Override
	public void map(NullWritable key, Text value, OutputCollector<Text, BytesWritable> output, Reporter report)
			throws IOException {
		try{

			System.out.println("Start Map");

			FSDataInputStream currentStream;
			BufferedReader currentReader;
			FileSystem fs;

			Path path = new Path(value.toString());
			fs = path.getFileSystem(conf);
			currentStream = fs.open(path);
			System.out.println("path: "+path);
  			currentReader = new BufferedReader(new InputStreamReader(currentStream));
  			
  			
  			Util_functions_khop util = new Util_functions_khop();
  			
  			System.out.println("Start read file");
  			util.readDBForMap(currentReader);
  			

  			for (Map.Entry<Integer, Node> entry : util.nodeList.entrySet()) {
  		        
  				
  				int id = entry.getKey();
  				Node node = entry.getValue();
  				System.out.println(id+ ":" + entry.getValue());
  				
  				Self_Inf self = new Self_Inf(node, new ArrayList());
  				Map<Integer,List<Edge_Inf>> k_hop= new HashMap<Integer, List<Edge_Inf>>();
  				List<Edge_Inf> edge_k_hop = new ArrayList();
  				k_hop.put(k, edge_k_hop);
  				self.setK_hop(k_hop);
  		    
  				String suffix= util.getSuffix(node);
				
				//create outputKey/value												
				Mapper_Key outKey = new Mapper_Key(id,suffix);
				Node_information node_inf = new Node_information(self,util.vid_outedge.get(id));
				Map<Integer,List<Edge_Inf>> k_inEdge = new HashMap<Integer, List<Edge_Inf>>();
				k_inEdge.put(k, util.vid_inedge.get(id));
				
			
				node_inf.setK_inEdge(k_inEdge);
				
				
				
				Mapper_Value outValue = new Mapper_Value(node_inf);							
				//write output data
				
				//output.collect(outKey.toText(), outValue.toBytesWritable());
				output.collect(outKey.toText(), outValue.toBytesWritable());
			}
  			
  			System.out.println("end of Map");

			
			
		}catch(Exception ex){
			System.out.println("mapperReader map: Exception "+ex.getMessage());
			ex.printStackTrace(System.out);
			throw ex;
		}
	}


	
}
