package EdgePartitioning;
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
import khop.Edge_Inf;

public class EdgePartition_Reduce extends MapReduceBase implements Reducer<Text, BytesWritable, Text, BytesWritable> {

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
	    this.conf = job;
	    util = new Util_functions_khop();
	    file = util.createFile(path, "partition.txt");
    }
	@SuppressWarnings("unchecked")
	@Override
	public void reduce(Text symbol, Iterator<BytesWritable> values, OutputCollector<Text, BytesWritable> output, Reporter reporter) throws IOException {
		// TODO Auto-generated method stub
		try{
			
			List<Edge_Inf> total = new ArrayList();
			while(values.hasNext())
				{
					
					List<Edge_Inf> edgeList = null;
					BytesWritable value = values.next();
					
					try{
						ByteArrayInputStream byteIn = new ByteArrayInputStream(value.getBytes());
	    				ObjectInputStream in = new ObjectInputStream(byteIn);
	     				
	    				edgeList =(List<Edge_Inf>)in.readObject();
	    				total.addAll(edgeList);
	     				/*System.out.println("---Start Each value:");
	     				node_inf.printInfor();
	     				System.out.println("---End Each value:");*/
	     				in.close();
	     				byteIn.close();	    
	     					     				     				
					}
					catch(ClassNotFoundException c)
	  				{
	     				System.out.println(" not found.");
	     				c.printStackTrace();
	  				}	
								
				}

					
					EdgePartitionMapper_Value outValue = new EdgePartitionMapper_Value(total);			
		
	 				String text = util.writeAText(total);
	 				if(text!=null)
	 					util.writeToFile_append(file, text);
	 				
	 				//System.out.println("---End printing Final each key value:");
	 			
	 				output.collect(symbol, outValue.toBytesWritable());	 				
				
			
		}catch(Exception ex){
			System.out.println("error reduce: "+ex.getMessage());
			ex.printStackTrace(System.out);
			throw ex;
		}
	}
	
	
			

}
