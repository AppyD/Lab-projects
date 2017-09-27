# Task 1: Function to detect which disks in an array overlap with a given disk
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt


# Creates an array of random x-y coordinates between 0 and 1
R = np.random.uniform(size=(20,2)) 
print R

# Function to determine all the overlapping disks in a given array
# Iterates over array twice to compare each disk with every other disk
def overlap(C, radius=0.05):
    for t in range(0,20):
        for i in range(0,20):
            if i == t:    # A disk being compared with itself
               break
            a = C[t,0] - C[i,0]
            b = C[t,1] - C[i,1]
            if ((a**2) + (b**2))**0.5 < 2*radius:
               print t, C[t], i, C[i]
               

#Function to plot the disks on a graph
def plot_disks(C):    
    for i in range(0,20):
		x = C[i,0]
		y = C[i,1]
		plt.axis('equal')
		ax = plt.gca()
		disk = plt.Circle((x,y), 0.05, edgecolor = 'k', facecolor=(0,0,1,0.5),)
		ax.add_patch(disk)
    plt.axis([0,1,0,1])
    plt.show()

clusters = {}   #dictionary of ALL clusters; contains nested single{} dictionaries
single = {'disks':[], 'left':False, 'right':False}   #dictionary for one cluster

def overlap_2(C, radius=0.05):
    temp = 0
    for t in range(0,20):
        for i in range(0,20):
            if i == t:    # A disk being compared with itself
               break
            a = C[t,0] - C[i,0]
            b = C[t,1] - C[i,1]
            if ((a**2) + (b**2))**0.5 < 2*radius:
				single = {'disks':[], 'left':False, 'right':False}   #dictionary for one cluster
				single['disks'] = (t, i)
				if C[t,0] - radius < 0 or C[i,0] - radius < 0:
					single['left'] = True
				if C[t,0] + radius > 1 or C[i,0] + radius > 1:
					single['right'] = True
				clusters[temp] = single
				temp += 1
    print clusters