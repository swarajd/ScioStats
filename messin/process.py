import csv
import numpy as np
datafile = open('stats2.csv', 'r')
datareader = csv.reader(datafile, delimiter=',')
data = []
for row in datareader:
    row = list(map(
        float,
        row
    ))
    data.append(row)    

print(np.array(data).T.tolist())