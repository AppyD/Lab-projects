import random
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import Project_A as PA

print "Enter second radius."
r2 = float(raw_input())

Disk2 = []

for i in range(0,PA.N):
    Disk2.append((np.random.uniform(size=(1,2)), random.choice([PA.radius,r2])))

clusters = []

# Function to plot disks of different radii.
# Changes from previous plot function: different x,y coordinate indexes
#                                      plots different radii in different colours

def plot_disks_rad(d_array):
    for i in range(0,PA.N):
        rad = d_array[i][1]
        x = d_array[i][0][0][0]    #x-coordinate of disk
        y = d_array[i][0][0][1]    #y-coordinate of disk
        plt.axis('equal')
        ax = plt.gca()
        if rad == PA.radius:
            circle = plt.Circle((x,y), rad, edgecolor = 'k', 
                                            facecolor=(1,0,0,0.5),)
        else:
            circle = plt.Circle((x,y), rad, edgecolor = 'k', 
                                            facecolor=(0,0,1,0.5),)
        ax.add_patch(circle)
    plt.axis([0,1,0,1])
    plt.show()


# Function to find overlapping disks of different radii.
# Changes from previous overlap function: x,y coordinates have different indexes
#                                         overlap condition is different

def overlap_rad(d_array,id):
    for t in range(0,PA.N):
        if t == id:
            break
        rad1 = d_array[t][1]
        rad2 = d_array[id][1]
        a = d_array[t][0][0][0] - d_array[id][0][0][0]
        b = d_array[t][0][0][1] - d_array[id][0][0][1]
        if ((a**2)+(b**2))**0.5 < (rad1+rad2):
            single = {'disks':[], 'left':False, 'right':False}
            single['disks'] = [t, id]
            if d_array[t][0][0][0] - rad1 < 0 or d_array[id][0][0][0] - rad2 < 0:
                single['left'] = True
            if d_array[t][0][0][0] + rad1 > 1 or d_array[id][0][0][0] + rad2 > 1:
                single['right'] = True
            clusters.append(single.copy())

global spans
global new_array
spans = []
new_array = []

# Function to return a list of all clusters in the system.
# Mostly unchanged from previous function but now calls new overlap function.

def findclusters_rad(d_array):
    for i in range(0,PA.N):
        overlap_rad(d_array,i)
    for j in range(0,PA.N):
        PA.whichcluster(clusters, j)
        for k in PA.connected:
            PA.joincluster(clusters[PA.connected[0]],clusters[k])
    repeats = []
    for f in clusters:
        a = f['disks']
        for g in clusters:
            if g == f:
                break
            b = g['disks']
            if any(i in b for i in a):
                repeats.append(clusters.index(f))
    repeats = list(set(repeats))
    repeats.sort()        
    repeats.reverse()
    for i in repeats:
        clusters.remove(clusters[i])
    #plot_disks_rad(Disk)


# Function to search for spanning clusters over various values of N.
# Modified to call the newer functions and create array with different radii.

def replot_rad(num_loops,density=PA.N):    
    for i in range(0,num_loops):
        global clusters
        global n_value
        n_value = density
        for p in range(0,200):
            for temp in range(0,n_value):        #create new_array list of coordinates
                new_array.append((np.random.uniform(size=(1,2)), 
                                            random.choice([PA.radius,r2])))
            findclusters_rad(new_array)
            PA.find_span(clusters)
            n_value += 1
            for f in clusters:
                clusters.remove(f)
    print "spans:", spans


# Function to plot spanning cluster in another colour on pyplot graph.
# Takes as argument: index of span in clusters list

def color_span_plot(span_id):
    for i in clusters[span_id]['disks']:
        rad = Disk2[i][1]
        x = Disk2[i][0][0][0]
        y = Disk2[i][0][0][1]
        plt.axis('equal')
        ax = plt.gca()
        circle = plt.Circle((x,y), rad, edgecolor = 'k', 
                                            facecolor=(0,1,0,0.5))
        ax.add_patch(circle)
        plt.axis([0,1,0,1])