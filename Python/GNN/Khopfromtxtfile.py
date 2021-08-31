import numpy as np
import pandas
import io


def generate_lines(filePath, delimiters=[]):
    with open(filePath) as f:

        for line in f:
            line = line.strip()  # removes newline character from end

        for d in delimiters:
            line = line.replace(d, " ")

            yield line


gen = generate_lines("2hop.txt", ["\n",","])

data = np.genfromtxt(gen, dtype= str, delimiter='-')



# edges = np.char.split(data, sep =',')
# nbr = np.char.split(edges,sep='-')
print("\n", data)
# print("\n", edges)