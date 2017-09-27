import numpy as np
import scipy as sp
import matplotlib as plt

C = np.random.uniform(size=(20,2))

def simple_overlap(C, radius=0.05):
    temp = 0
    clusters = {}
    for t in range(0,20):
        for i in range(0,20):
            if i == t:    # A disk being compared with itself
               break
            a = C[t,0] - C[i,0]
            b = C[t,1] - C[i,1]
            if ((a**2) + (b**2))**0.5 < 2*radius:
                clusters[temp] = (C[t], C[i])
                temp += 1
    print clusters