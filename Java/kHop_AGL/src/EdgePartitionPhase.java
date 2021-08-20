import java.util.*;
import java.io.*;
import java.lang.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapred.lib.IdentityReducer;
import org.apache.hadoop.util.*;

import EdgePartitioning.EdgePartition_Map;
import EdgePartitioning.EdgePartition_Reduce;
import kHop.Util.MyInputFormat;
import khop.Khop_Map;
import khop.Khop_MapForKTime;
import khop.Khop_Reduce;
import sfsm.miningphase1.FrequentSN_Map;
import sfsm.miningphase1.FrequentSN_Reduce;


import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.io.compress.CodecPool;
import org.apache.hadoop.io.compress.CompressionCodec;
import org.apache.hadoop.io.compress.Compressor;

public class EdgePartitionPhase extends Configured implements Tool{
	
	public static void main(String[] args) throws Exception {
		System.exit(ToolRunner.run(new EdgePartitionPhase(), args));
		
	}

	@Override
	public int run(String[] args) throws Exception {
		// TODO Auto-generated method stub
		
		if (args.length < 2) {
				System.err.println("Usage: "+" <in> <output> <noOfPart>");
				
				return -1;
		}
		String intput_dir = args[0];
		String output_dir = args[1];
		

		String partNum = args[2];
		
		JobConf conf1  = new JobConf(getConf(),EdgePartitionPhase.class);
		
		conf1.setInputFormat(MyInputFormat.class);
		conf1.setMapperClass(EdgePartition_Map.class); 
		conf1.setReducerClass(EdgePartition_Reduce.class); 
		
		conf1.setMapOutputKeyClass(Text.class);
		conf1.setMapOutputValueClass(BytesWritable.class);
		conf1.setOutputKeyClass(Text.class);
	
		conf1.setOutputValueClass(BytesWritable.class);
		conf1.setOutputFormat(SequenceFileOutputFormat.class);
			
		conf1.set("mapred.task.timeout","7200");
			
		conf1.set("mapred.output.compress", "true");
		conf1.set("mapred.output.compression.codec", "org.apache.hadoop.io.compress.BZip2Codec");
		conf1.set("partNum", partNum);
        
	    conf1.setNumMapTasks(Integer.parseInt(args[3]));
		conf1.setNumReduceTasks(Integer.parseInt(args[4]));
		
		
		conf1.set("output_writeTofile_path", output_dir+".textFile");
		
		FileInputFormat.addInputPaths(conf1, intput_dir); 
		
		FileOutputFormat.setOutputPath(conf1, new Path(output_dir+"/partition"));

		RunningJob job1 = myCustomRunJob(conf1);

		return 0;
	}
	
	public static RunningJob myCustomRunJob(JobConf job) throws Exception {
	    JobClient jc = new JobClient(job);
	    RunningJob rj = jc.submitJob(job);
	    if (!jc.monitorAndPrintJob(job, rj)) {
	      throw new IOException("Jobr failed with info: " + rj.getFailureInfo());
	    }
	    return rj;
	}
	
	boolean deleteDirectory(File directoryToBeDeleted) {
	    File[] allContents = directoryToBeDeleted.listFiles();
	    if (allContents != null) {
	        for (File file : allContents) {
	            deleteDirectory(file);
	        }
	    }
	    return directoryToBeDeleted.delete();
	}
	
}
