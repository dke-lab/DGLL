from pydoop.hdfs import hdfs
import pydoop.mapreduce.api as api
import pydoop.mapreduce.pipes as pp
import sys
class Mapper(api.Mapper):
    def map(self, context):
        print("IRFAN KHOP NEW Mapper")
        inNodeList = list()
        # {nodeId:[[inNodes]]}
        targetNodeConn = {}
        sNode, dNode = context.value.split("\t")
        dNode = dNode.strip()      
        # inNodes Addition
        if dNode not in targetNodeConn.keys():
            targetNodeConn[dNode] = list()
            targetNodeConn[dNode].append(sNode)
        else:
            targetNodeConn[dNode].append(sNode)
        context.emit(dNode, targetNodeConn[dNode])


class Reducer(api.Reducer):
    def reduce(self, context):
        print("IRFAN KHOP NEW Reducer")
        fs = hdfs("localhost", 9000) 
        k = 1
        if not fs.exists("/khop/khop_number.txt"):
            print("khop_main.py is not executed correctly:")
            sys.exit()
        f = fs.open_file("/khop/khop_number.txt", 'rt')
        khop = int(f.read())
        f.close()
        if khop < 0:
            print("khop should be greater than zero: default is 1.", khop)
            khop = 1
        if k == khop:
            directory = "/khop"
            if not fs.exists(directory):
                fs.create_directory(directory)
            fileName = str(context.key) + "_" + str(k) +".txt"
            path = directory + "/" + fileName
            self.oneHopGeneration(context, fs, path) 
        else:
            path = "/khop/tmp/"
            directory = "/tmp" + str(k) + "hop"
            print(path + directory)
            if not fs.exists(path + directory):
                fs.create_directory(path + directory)
            fileName = str(context.key) + "_" + str(k) +".txt"
            # path + directory + "/" +  fileName
            self.oneHopGeneration(context, fs, path + directory + "/" + fileName) 

     

    def oneHopGeneration(self, context, fs, path):
        if fs.exists(path):
            f = fs.open_file(path, "at")
        else:
            f = fs.open_file(path, "wt")
        if context.values != []:
            for c in context.values:
                # print(c[0], "-->", context.key)
                f.write(str(c[0]) + "\t" +  str(context.key) + "\n")
        f.close()
    
    
   


def __main__():
    pp.run_task(pp.Factory(Mapper, Reducer))

