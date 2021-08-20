import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.InputStreamReader;

import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

import kHop.Util.Util_functions_khop;

public class EdgeParitioning {
	private static Util_functions_khop util;

	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub
		if (args.length < 2) {
			System.err.println("Usage: "+" <inFile> <output> <no of partition>");
		
		}
		String intput = args[0];
		String output_dir = args[1];
		
	
		int partNum = Integer.parseInt(args[2]);
		
		FSDataInputStream currentStream;
		BufferedReader currentReader;
		File file = new File(intput);
		System.out.println("path: "+ intput);
			currentReader = new BufferedReader(new FileReader(file));
			
		util = new Util_functions_khop();
		
		util.readDBForMap(currentReader);
		
		}

}
