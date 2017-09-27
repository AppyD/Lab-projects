import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import Project_A as PA

Disk3D = np.random.uniform(size=(PA.N,3))

clusters = []   # list of ALL clusters; each element is a dictionary.

# Function to plot the array of disks
# Takes as arguments: array of disk coordinates
#                     radius of disks

def plot_disks_3D(d_array, r=radius):
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for i in range(0,N):
        x = d_array[i,0] + radius*np.cos(u)*np.sin(v)    # x-coordinate of sphere centre
        y = d_array[i,1] + radius*np.sin(u)*np.sin(v)    # y-coordinate of sphere centre
        z = d_array[i,2] + radius*np.cos(v)    # z-coordinate of sphere centre
        ax.plot_wireframe(x, y, z, color='r')
        ax.set_aspect("equal")
    plt.show()


# Function to find overlapping spheres with a fixed radius
# Changes from previous function: modified overlap condition to 3 dimensions

def overlap_3D(d_array,id):
    for t in range(0,N):
        if t == id:        #avoid comparing a disk with itself
            break
        a = d_array[t,0] - d_array[id,0]
        b = d_array[t,1] - d_array[id,1]
        c = d_array[t,2] - d_array[id,2]
        if ((a**2)+(b**2)+(c**2))**0.5 < 2*radius:    # overlap condition
            single = {'disks':[], 'left':False, 'right':False}
            single['disks'] = [t, id]
            if d_array[t,0] - radius < 0 or d_array[id,0] - radius < 0:
                single['left'] = True           # cluster touches left boundary
            if d_array[t,0] + radius > 1 or d_array[id,0] + radius > 1:
                single['right'] = True          # cluster touches right boundary
            clusters.append(single.copy())


# Function to return a list of all clusters in the system.
# Changes from previous function:

def findclusters_3D(d_array, r=radius):
    for i in range(0,PA.N):
        overlap_3D(d_array,i)
    for j in range(0,PA.N):
        PA.whichcluster(clusters, j)
        for k in PA.connected:
            PA.joincluster(clusters[PA.connected[0]],clusters[k])
    repeats = []            # clusters to be deleted after amalgamation
    for f in clusters:
        a = f['disks']
        for g in clusters:
            if g == f:
                break
            b = g['disks']
            if any(i in b for i in a):
                repeats.append(clusters.index(f))
    repeats = list(set(repeats))    # remove duplicates in list
    repeats.sort()        
    repeats.reverse()     # delete in reverse to avoid mismatching indices
    for i in repeats:
        clusters.remove(clusters[i])
    #print clusters


global spans
global new_array
spans = []        #list of N values for which a spanning cluster was obtained
new_array = []    #empty list to be filled with new disk arrays


# Function to search for spanning clusters over various values of N.
# Changes from previous function: modified dimensions of new array

def replot_3D(num_loops,density=PA.N,r=radius):
    for i in range(0,num_loops):
        global clusters
        global n_value
        n_value = PA.N
        for i in range(0,200):
            new_array = np.random.uniform(size=(n_value,3))
            PA.findclusters(new_array)
            PA.find_span(clusters)
            n_value += 1
            for i in clusters:
                clusters.remove(i)
    print "spans:", spans