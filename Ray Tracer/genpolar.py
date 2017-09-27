"""Module to generate pairs of polar coordinates that are equally spaced within a specified radius."""

import numpy as np

#R is a list of radii, N is a list of the number of angles for each radius in R.
def rtpairs(R,N):
	x = 2*np.pi
	count = 0
	for i in N:
		for j in range(0,i):
			r = R[count]
			t = j*x/(i)
			yield r,t
		count += 1

def rtuniform(n,rmax,m):
    R = []
    N = []
    for i in range(0,n+1):
        r = i*rmax/n
        R.append(r)
        if i == 0:
            ni = 1
        else:
            ni = m*i
        N.append(ni)
    return rtpairs(R,N)