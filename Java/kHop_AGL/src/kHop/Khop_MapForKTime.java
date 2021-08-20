package khop;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.List;

import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.MapWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

import kHop.Util.Util_functions_khop;

public class Khop_MapForKTime extends MapReduceBase implements Mapper<Text, BytesWritable, Text, BytesWritable>	{


	private JobConf conf;
	private int k;

	@Override
	public void configure(JobConf conf)
	{
		this.conf = conf;
		String kValue = conf.get("k");
	    k = Integer.parseInt(kValue);		
	}

	public void map(Text key, BytesWritable value, OutputCollector<Text, BytesWritable> output, Reporter reporter)
			throws IOException {
		//System.out.println("-------------- begin mapper: map, key: " + key + "------------");

		long start = System.currentTimeMillis();

		Text map_value = new Text();

		Node_information node_inf = null;
		try {
			ByteArrayInputStream sbufIn = new ByteArrayInputStream(value.getBytes());
			ObjectInputStream in = new ObjectInputStream(sbufIn);
			node_inf = (Node_information) in.readObject();

			in.close();
			sbufIn.close();
		} catch (ClassNotFoundException c) {
			System.out.println("not found.");
		}

		List<Edge_Inf> edge_k_hop = new ArrayList();
		node_inf.getSelf().getK_hop().put(k, edge_k_hop);
		Mapper_Value outValue = new Mapper_Value(node_inf);
		
/*
		System.out.println("k-hop_mapper output: key='"+key+"'");
		node_inf.printInfor();		*/		

		output.collect(key, outValue.toBytesWritable());				
		
		
		//System.out.println("-------------- end mapper: map, key: " + key + "------------");
	}


			
	}


	

