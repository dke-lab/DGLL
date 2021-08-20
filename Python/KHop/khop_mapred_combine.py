from pydoop.hdfs import hdfs
class hdfsCombineReducer:
    def deleteTmpFiles(self, fs, path):
        fs.delete(path)
        fs.delete("/khop/khop_number.txt")
    def k_hop(self, fs, khop, path):
        # get list of nodes from tmpkhop
        directory = "tmp" + str(khop) + "hop/"
        allNodesListTmpKHop = fs.list_directory(path + directory)
        # create directory for stroing output
        for n in range(len(allNodesListTmpKHop)):
            node = allNodesListTmpKHop[n]["name"].split("/")[-1].split(".")[0].split("_")[0]
            # Merge All ks(1,2,  3, ..., k) hops from all tmpkhop folders where k = 1, 2, 3, ...., khop
            targetAdjacenNodesList = ""
            for k in range(1, khop+1):
                txt = fs.open_file(path + "tmp" + str(k) + "hop/"  + str(node) + "_" + str(k) + '.txt', "rt")
                txt =  txt.read()
                targetAdjacenNodesList += txt
            targetAdjacenNodesList = targetAdjacenNodesList.split("\n")
            targetAdjacenNodesList = list(set(targetAdjacenNodesList))
            targetAdjacenNodesList = list(filter(None, targetAdjacenNodesList))
            targetAdjacenNodesList = '\n'.join([str(e) for e in targetAdjacenNodesList])
            targetAdjacenNodesList = targetAdjacenNodesList + '\n'
            fileName =  str(node) + "_" + str(khop) + '.txt'
            f_new = fs.open_file(path.replace("/tmp", "") + fileName, "wt")
            f_new.write(targetAdjacenNodesList)
            f_new.close()
        self.deleteTmpFiles(fs, path)
    def tmpk_hop(self, fs, khop, path):
        k = 2
        while k <= khop:
            pathToTmpDir = ""
            directory = "tmp" + str(k) + "hop/"
            pathToTmpDir = path + directory
            # print(pathToTmpDir)
            if not fs.exists(pathToTmpDir):
                fs.create_directory(pathToTmpDir)
            # if not os.path.exists(pathToTmpDir):
            #     os.mkdir(pathToTmpDir)
            # rm -r khop && mkdir khop && mkdir khop/tmp && cp -r tmp1hop khop/tmp && ls khop/tmp/tmp1hop/
            # get nodes from the k-1 hop list
            directory = "tmp" + str(k-1) + "hop/"
            nodesList = fs.list_directory(path + directory)
            for i in range(len(nodesList)):
                node = nodesList[i]["name"].split("/")[-1].split(".")[0]
                f = fs.open_file(path + directory  + str(node)  + '.txt' , "rt")
                targetAdjacenNodesList = f.read()
                f.close()
                targetAdjacenNodesList = list(filter(None, targetAdjacenNodesList.split("\n")))
                nodesAtKhopFromNode = ""
                # Neighbours of nodes that are adjacent(neigbours) to targent node; neighbours of neighbors of nodes 
                for i in targetAdjacenNodesList:
                #  1 hop folder for getting onehop neighbours of a node
                    pathOneHop = path + "tmp" + str(1) + "hop/"  + str(i.split("\t")[0]) + '_' + str(1) + '.txt'
                    if fs.exists(pathOneHop):
                        f = fs.open_file(pathOneHop, 'rt')
                        nodesAtKhopFromNode += f.read()
                        f.close()
                if nodesAtKhopFromNode == "":
                    continue
                fileName = str(node.split("_")[0]) + '_' + str(k) + '.txt'
                f_new = fs.open_file(pathToTmpDir + fileName, "wt")
                f_new.write(nodesAtKhopFromNode)
                f_new.close()
            k += 1
        self.k_hop(fs, khop, path)
        
    def reducer(self):
        fs = hdfs("localhost", 9000)
        khop = 3
        if khop < 1:
            print("khop should be greater than zero: default is 3")
            khop = 3
        # folder for savign temporary files
            # folder for khop generation
        path = ""
        if khop == 1:
            print("create first neibhbour hood because k == khop")
        else:
            path = path + "/khop/tmp/"
            self.tmpk_hop(fs, khop, path)
obj = hdfsCombineReducer()
obj.reducer()

