import numpy as np
import csv
import os

mylist=np.arange(0,int('200'),step=1)
file=os.getcwd()+'\prueba.csv'
print(file)

with open(file, 'wb') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(mylist)
