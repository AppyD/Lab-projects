import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import task1
import task2

C = np.random.uniform(size=(20,2)) 
clusters = {}   #dictionary of ALL clusters; contains nested single{} dictionaries
#single = {'disks':[], 'left':False, 'right':False}   #dictionary for one cluster

task1.plot_disks(C)
task1.overlap(C)
task1.overlap_2(C)

def whichcluster(c_list, disk_id):
	for i in c_list:
		if disk_id in c_list[i]:
			 print i
	print c_list