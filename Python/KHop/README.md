# KHop
Generating KHop in the MapReduce Infrastructure.
# Requirement
- Python 3.6.9
- Pydoop 2.0.0
- Hadoop 3.3.1

# Run the code
You can run the code using the following command:

```
python khop_main.py Khop "path/inuptgraph" "path/khop"
```

Where 
- Khop: required khop number
- path/inputgraph: hdfs path to the input graph
- path/khop: hdfs path to the output

# Output:
After running the code successfully, all the generated khops will be stored in "/khop" on hdfs as:

NodeID_KHop.txt

Provided for academic use only
