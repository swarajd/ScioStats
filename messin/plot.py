import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

def read_datafile(file_name):
    # the skiprows keyword is for heading, but I don't know if trailing lines
    # can be specified
    data = np.loadtxt(file_name, delimiter=',')
    return data

data = read_datafile('stats2.csv')

x= data[:,0]
y= data[:,1]

plt.title('number of medals vs average rank')    
plt.xlabel('number of medals')
plt.ylabel('average rank')

plt.plot(x,y, 'ro', label='the data')

leg = plt.legend()

plt.show()