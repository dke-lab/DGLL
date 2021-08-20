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

public class GraphMiningPhase extends Configured implements Tool{
	
	public static void main(String[] args) throws Exception {
		System.exit(ToolRunner.run(new GraphMiningPhase(), args));
		
	}

	@Override
	public int run(String[] args) throws Exception {
		// TODO Auto-generated method stub
		
		if (args.length < 2) {
				System.err.println("Usage: "+" <in> <output> <minsup><no_of_mapper><no_of_reducer><k>");
				
				return -1;
		}
		String intput_dir = args[0];
		String output_dir = args[1];
		

		String minsup = args[2];
		int k = Integer.parseInt(args[5]);
		
		JobConf conf1  = new JobConf(getConf(),GraphMiningPhase.class);
		
		conf1.setInputFormat(MyInputFormat.class);
		conf1.setMapperClass(Khop_Map.class); 
		conf1.setReducerClass(Khop_Reduce.class); 
		
		conf1.setMapOutputKeyClass(Text.class);
		conf1.setMapOutputValueClass(BytesWritable.class);
		conf1.setOutputKeyClass(Text.class);
	
		conf1.setOutputValueClass(BytesWritable.class);
		conf1.setOutputFormat(SequenceFileOutputFormat.class);
			
		conf1.set("mapred.task.timeout","7200");
			
		conf1.set("mapred.output.compress", "true");
		conf1.set("mapred.output.compression.codec", "org.apache.hadoop.io.compress.BZip2Codec");
		conf1.set("minsup", minsup);
        
	    conf1.setNumMapTasks(Integer.parseInt(args[3]));
		conf1.setNumReduceTasks(Integer.parseInt(args[4]));
		
		conf1.set("k", "1");
		
		conf1.set("output_writeTofile_path", output_dir+".textFile");
		
		FileInputFormat.addInputPaths(conf1, intput_dir); 
		
		FileOutputFormat.setOutputPath(conf1, new Path(output_dir+"/k1"));

		RunningJob job1 = myCustomRunJob(conf1);
		
		int iterationCount=1;
		if(k>1)
		{
			while(true)
			{
				String input;
				if (iterationCount == 1)
					input = output_dir+"/k1";
				else
					input = output_dir+"/k" + iterationCount;
	
				String output = output_dir+"/k" + (iterationCount + 1);

				JobConf conf2  = new JobConf(getConf(),GraphMiningPhase.class);								
				
				conf2.setInputFormat(SequenceFileInputFormat.class);
				conf2.setMapperClass(Khop_MapForKTime.class);
				conf2.setReducerClass(Khop_Reduce.class);

				conf2.setMapOutputKeyClass(Text.class);
				conf2.setMapOutputValueClass(BytesWritable.class);
				
				conf2.setOutputKeyClass(Text.class); 			
				conf2.setOutputValueClass(BytesWritable.class);
				conf2.setOutputFormat(SequenceFileOutputFormat.class);
				
				conf2.set("k", String.valueOf(iterationCount + 1));
				
				conf2.set("mapred.task.timeout","1800000000");
				conf2.set("mapreduce.map.log.level", "DEBUG");
				conf2.set("mapreduce.reduce.log.level", "DEBUG");

				conf2.set("output_writeTofile_path", output_dir+".textFile");
				
					
				conf2.setNumMapTasks(Integer.parseInt(args[3]));
				conf2.setNumReduceTasks(Integer.parseInt(args[4]));
				FileInputFormat.addInputPath(conf2, new Path(input));
				FileOutputFormat.setOutputPath(conf2, new Path(output));
				
				//RunningJob job = JobClient.runJob(conf2);
				RunningJob job = myCustomRunJob(conf2);
				Counters counters = job.getCounters();
				
				iterationCount++;
				if(iterationCount == k)
					break;
				
			}
		
		}
	
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
