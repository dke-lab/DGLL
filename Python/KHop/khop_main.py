# how to run
#  python khop_main.py "/home/thesun/hdoop/code/" 3 "/input/graph_cora.txt" "/output"
# python khop_main.py "path to code"
import os
import sys
from pydoop.hdfs import hdfs
fs = hdfs("localhost", 9000) 
khop = sys.argv[1]
pathToInputData = str(sys.argv[2])
pathToOutputData = str(sys.argv[3])
# path to khop folder where output will be shown
pathToKHop = "/khop"
pathToKhopMapRed = "khop_mapred.py"
pathToKhopMapRedCombine = "khop_mapred_combine.py"

if not (os.path.exists(pathToKhopMapRed) or fs.exists(pathToKhopMapRed)):
	print("khop_mapred.py file not found:", pathToKhopMapRed)
	sys.exit()

if not (os.path.exists(pathToKhopMapRedCombine) or fs.exists(pathToKhopMapRedCombine)):
	print("khop_mapred_combine.py file not found:", pathToKhopMapRedCombine)
	sys.exit()

if not khop.isdigit():
	print("Khop number error", khop)
	sys.exit()

if not (os.path.exists(pathToInputData) or fs.exists(pathToInputData)):
	print("No input file or directory:", pathToInputData)
	sys.exit()
if not fs.exists(pathToKHop):
    fs.create_directory(pathToKHop)

f = fs.open_file(pathToKHop + "/khop_number.txt", 'wt')
f.write(str(khop))
f.close()
os.system("pydoop submit --upload-file-to-cache " + pathToKhopMapRed + " " + "khop_mapred.py.py".split(".")[0] + " " + pathToInputData + " " + pathToOutputData)
os.system("python " + pathToKhopMapRedCombine)
print("Info: All khops will be stored on HDFS under the folder /khop.")
