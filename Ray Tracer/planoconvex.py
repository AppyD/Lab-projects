"""Module to implement the raytracer model and propagate a bundle of rays through different refractive media."""

import matplotlib.pyplot as plt
import raytracer as rt
import genpolar as gp
import numpy as np

#Lens definitions for first and second orientations respectively

SR1 = rt.SphericalRefraction(100.0, 0ol0o, 1.0, 1.5168, 10.0) #plane surface first
SR2 = rt.SphericalRefraction(105.0, -0.02, 1.5168, 1.0, 10.0) #negative curvature

SR3 = rt.SphericalRefraction(100.0, 0.02, 1.0, 1.5168, 10.0) #positive curvature
SR4 = rt.SphericalRefraction(105.0, 0, 1.5168, 1.0, 10.0) #plane surface second


def findzintercept(lens1,lens2):
    """Finds intersection point of ray with z-axis"""

    TR = rt.Ray([0.1,0.1,80],[0.0,0.0,1.0]) #test ray close to z-axis
    lens1.propagate_ray(TR)
    lens2.propagate_ray(TR)
    ratio = -(TR._p[0])/(TR._k[0])
    intercept = TR._p + (ratio*TR._k)
    return intercept


def findrms(raylist):
    """Finds rms value of a bundle of rays"""

    sum = 0
    for item in raylist:
        sum += (item._p[0]**2 + item._p[1]**2)
    rms = (sum/len(raylist))**0.5
    print "The RMS value is %g mm." % rms    

                        
def plotspots(a=1):
    """Produces three plots: 
    1) Spot diagram of initial bundle of rays in x-y plane. 
    2) Ray diagram in x-z plane showing rays passing through the lens.
    3) Spot diagram of ray bundle at the output plane i.e. the detector.
    Produces plots for either orientation of the lens depending on a.""" 
    
    if a == 1:
        lens1 = SR1
        lens2 = SR2
        
    else:
        lens1 = SR3
        lens2 = SR4
        
    x = findzintercept(lens1,lens2)
    focal = x[2]
    output = rt.OutputPlane(focal)
    print "Focal length for orientation %g is %g mm." % (a, focal)
    
    bundle = []    
    
    for r,t in gp.rtuniform(7, 5.0, 6): #rmax (5.0) must be a float
        xcoord = r*np.cos(t)
        ycoord = r*np.sin(t)
        
        ray = rt.Ray([xcoord,ycoord,0.0],[0.0,0.0,0.1])
        lens1.propagate_ray(ray)
        lens2.propagate_ray(ray)
        output.propagate_ray(ray)
        bundle.append(ray)
        
        plt.figure(a)
       
        if a == 1:
            plt.suptitle('Planoconvex Lens Orientation 1', size=16)
        else:
            plt.suptitle('Planoconvex Lens Orientation 2', size=16)
        
        ax1 = plt.subplot(2,2,1)
        ax1.plot(xcoord, ycoord, 'bo')
        ax1.set_title('Bundle of Rays at Source, z=0', size=12)
        ax1.axis('equal')
        
        ax2 = plt.subplot(2,2,2)
        x2 = [j[2] for j in ray.vertices()]
        y2 = [j[0] for j in ray.vertices()]
        ax2.plot(x2,y2,'r-')
        ax2.set_title('Propagation of Rays in xz Plane', size=12)
    
    x3 = [j._p[0] for j in bundle]
    y3 = [j._p[1] for j in bundle]
    ax3 = plt.subplot(2,2,3)
    ax3.plot(x3,y3,'bo')
    ax3.set_title('Bundle of Rays at Focus', size=12)
    ax3.locator_params(nbins=5)
    ax3.axis('equal')

    findrms(bundle)
    
    difflim = ((588*10**(-9))*focal)/10.0
    print "The diffraction limit is %g m." % difflim


#Finds the focal length, rms and diffraction limit for both orientations
plotspots(1)
plotspots(2)