import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

print "Enter a number density."
N = int(raw_input())
print "Enter a disk radius."
radius = float(raw_input())

Disk = np.random.uniform(size=(N,2))

clusters = []   # list of ALL clusters; each element is a dictionary.


# Function to plot the array of disks
# Takes as arguments: array of disk coordinates
#                     radius of disks

def plot_disks(d_array, r=radius):
    for i in range(0,N):
        x = d_array[i,0]    # x-coordinate of disk
        y = d_array[i,1]    # y-coordinate of disk
        plt.axis('equal')
        ax = plt.gca()
        circle = plt.Circle((x,y), r, edgecolor = 'k', facecolor=(0,0,1,0.5),)
        ax.add_patch(circle)
    plt.axis([0,1,0,1])
    plt.show()


# Task 1: Function to detect which disks in an array overlap with a given disk.
# Takes as arguments: array of disk coordinates
#                     index of a specific disk within the array, e.g. 2

def overlap(d_array,id):
    for t in range(0,N):
        if t == id:        #avoid comparing a disk with itself
            break
        a = d_array[t,0] - d_array[id,0]
        b = d_array[t,1] - d_array[id,1]
        if ((a**2)+(b**2))**0.5 < 2*radius:    # overlap condition
            single = {'disks':[], 'left':False, 'right':False}
            single['disks'] = [t, id]
            if d_array[t,0] - radius < 0 or d_array[id,0] - radius < 0:
                single['left'] = True          # cluster touches left boundary
            if d_array[t,0] + radius > 1 or d_array[id,0] + radius > 1:
                single['right'] = True        # cluster touches right boundary
            clusters.append(single.copy())


# Task 2: Function that amalgamates two clusters.
# Takes as arguments: cluster 1
#                     cluster 2

def joincluster(c1, c2):
    c1['disks'] = c1['disks'] + c2['disks']
    c1['disks'] = list(set(c1['disks']))     #remove duplicates in list
    if c1['left'] or c2['left']:
        c1['left'] = True
    if c1['right'] or c2['right']:
        c1['right'] = True


# Task 3: Function to find which cluster a given disk belongs to.
# Takes as arguments: list of clusters
#                     index of specific disk
# "connected" is a list of indexes for clusters containing the specified disk.

def whichcluster(c_list, disk_id):
    global connected
    connected = []
    for m in c_list:
        for temp in m['disks']:
            if disk_id == temp:
                connected.append(c_list.index(m))


# Task 4: Function that returns a list of clusters.
# Takes as arguments: array of disk coordinates
#                     radius of disks
# Finds all disk overlaps in system, then amalgamates all connected clusters.
# Identifies repeats in the clusters list and deletes them.

def findclusters(d_array, r=radius):
    global connected
    for i in range(0,N):
        overlap(d_array,i)    #find all overlapping pairs of disks
    for j in range(0,N):
        whichcluster(clusters, j)
        for k in connected:
            joincluster(clusters[connected[0]],clusters[k])
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
spans = []        # list of N values for which a spanning cluster was obtained
new_array = []    # empty list to be filled with new disk arrays
span_percent = [] # percentage of spanning clusters found for each density

# Function to determine if a cluster spans the entire area.
# Takes as argument: list of all clusters (after amalgamation).

def find_span(c_list):
    global n_value
    for i in c_list:
        if i['left'] and i['right']:
            spans.append(n_value)


# Function to find spanning clusters for a particular N value numerous times	
# Takes as arguments: disk density
#                     number of times to loop (to generate a larger data set)
#                     radius of the disks

def replot(num_loops,density=N,r=radius):
    for i in range(0,num_loops):
        global clusters
        global n_value
        n_value = density
        new_array = np.random.uniform(size=(n_value,2))
        findclusters(new_array)
        find_span(clusters)
        clusters[:] = []
    #print "spans:", len(spans)
    
# Function to hunt for critical percolation threshold in a particular N range
# Takes as arguments: number of times to loop in replot_2 function
#                     disk density
#                     radius of the disks
def replot2(num_loops, density=N,r=radius):
    global n_value
    global clusters
    global span_percent
    for k in range(0,50):
        replot(num_loops,density)
        m = list(spans)
        span_percent.append((density,(float(len(m))/float(num_loops))*100))
        density += 1
        spans[:] = []
    print span_percent