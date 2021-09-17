package dgll.datalayer.storage;

import org.apache.commons.io.IOUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class Hdfs {
    FileSystem fs;

    public Hdfs(String url) throws IOException {
        Configuration configuration = new Configuration();
        configuration.set("fs.defaultFS", url);
        fs = FileSystem.get(configuration);
    }

    public List<String> list(String dir, boolean recursive) throws IOException {
        List<String> paths = new ArrayList<>();
        RemoteIterator<LocatedFileStatus> fileIter = fs.listFiles(new Path(dir), recursive);

        while (fileIter.hasNext()) {
            paths.add(fileIter.next().getPath().toString());
        }

        return paths;
    }

    public List<String> read(String path) throws IOException {
        Path hdfsReadPath = new Path(path);
        FSDataInputStream inputStream = fs.open(hdfsReadPath);

        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8));
        String line = null;
        List<String> lines = new ArrayList<>();

        while ((line=bufferedReader.readLine()) != null) {
            lines.add(line);
        }

        inputStream.close();

        return lines;
    }

    public void write(String path, String data) throws IOException {
        Path hdfsWritePath = new Path(path);
        FSDataOutputStream fsDataOutputStream = fs.create(hdfsWritePath,true);
        BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(fsDataOutputStream,StandardCharsets.UTF_8));
        bufferedWriter.write(data);
        bufferedWriter.close();
    }

    public void append(String path, String data) throws IOException {
        Path hdfsWritePath = new Path(path);
        FSDataOutputStream fsDataOutputStream = fs.append(hdfsWritePath);
        BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(fsDataOutputStream,StandardCharsets.UTF_8));
        bufferedWriter.write(data);
        bufferedWriter.close();
    }

    public void delete(String path) throws IOException {
        Path file = new Path(path);

        if (fs.exists(file)) {
            fs.delete(file, true);
        }
    }

    public boolean exists(String path) throws IOException {
        return fs.exists(new Path(path));
    }
}
