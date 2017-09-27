"""A module to build a 3D optical ray tracer."""
import numpy as np


class Ray:
    """Class representing an optical ray. p represents the position of the ray and k represents its direction."""
    
    def __init__(self, p=None, k=None):
        if np.size(p) != 3:
            raise Exception("Ray Position Parameter Size")
            
        if np.size(k) != 3:
            raise Exception("Ray Direction Parameter Size")
            
        self._p = np.array(p)
        self._k = np.array(k)
        
        if self._k[2] < 0:
            raise Exception("Left-going ray instead of right-going ray.")
            
        self._positions = [self._p]
        self._directions = [self._k]
        
    def __repr__(self):
        return "Ray: position=%s, direction=%s" % (str(self._p), str(self._k))
        
    def __str__(self):
        return "p(%g, %g, %g), k(%g,%g,%g)" % (self._p[0], self._p[1], 
        self._p[2], self._k[0], self._k[1], self._k[2])
                                
    def p(self):
        return self._p
        
    def k(self):
        return self._k
        
    def append(self, p, k):
        """ Adds a new point and direction to a given ray, and updates its current position and direction attributes."""
        
        p1 = np.array(p)
        k1 = np.array(k)
        
        if np.size(p) != 3:
            raise Exception("Ray Position Parameter Size")
            
        if np.size(k) != 3:
            raise Exception("Ray Direction Parameter Size")
            
        self._positions.append(p1)
        self._directions.append(k1)
        
        #update ray's current position and direction to those appended
        self._p = p1
        self._k = k1
    
    def vertices(self):
        return self._positions     
        
class OpticalElement:
    def propagate_ray(self, ray):
        "propagate a ray through the optical element"
        raise NotImplementedError()

class SphericalRefraction(OpticalElement):
    """ Defines the lens that rays are to be propagated through. Parameters are as follows: 
    z0 (point where the lens surface touches the z-axis)
    curvature (the curvature of the surface)
    n1 and n2 (the refractive indices on either side of the lens)
    aperture radius (maximum extent of surface from optical axis). """
    
    def __init__(self, z0=0.0, curvature=1.0, n1=1.0, n2=1.0, aperturerad=1.0):
        self._z0 = z0
        self._curvature = curvature
        self._n1 = n1
        self._n2 = n2
        self._aprad = aperturerad
        
        
        if self._curvature != 0:
            self._radius = np.abs((1/self._curvature))
            
        else:
            self._radius = aperturerad
        
        
        if self._curvature > 0:
            self._centreofcurv = np.array([0, 0, self._z0 + self._radius])

        elif self._curvature < 0:
            self._centreofcurv = np.array([0, 0, self._z0 - self._radius])
        
        else:
            self._centreofcurv = np.array([0, 0, self._z0])
        
        self._intersection = []
    
    def intercept(self, ray):
        """Finds first valid intersection point of incoming ray and lens"""
        
        #Geometry given in lab book
        if self._curvature == 0:
            zdiff = self._z0 - ray._p[2]
            khat = ray._k * (1/np.linalg.norm(ray._k))
            l = zdiff/khat[2]
            temp = ray._p + (l*khat)
            self._intersection = np.array(temp)
                
        else:
            r = ray._p - self._centreofcurv
            kmag = ray._k * (1/np.linalg.norm(ray._k))
            rmag = np.linalg.norm(r)
            inn = np.inner(r, kmag)
            distance1 = -inn + (inn**2 - (rmag**2 - self._radius**2))**0.5
            distance2 = -inn - (inn**2 - (rmag**2 - self._radius**2))**0.5
            
            if np.isnan(distance1) and np.isnan(distance2):
                self._intersection = None
                print "None"
                
            else:
                if self._curvature > 0:
                    distance = min(distance1, distance2)
                    
                else:
                    distance = max(distance1,distance2)
                    
                lvec = np.array((distance * kmag))
                temp = ray._p + lvec
                self._intersection = np.array(temp)
        
        #Ray only intersects if it is within the lens' aperture radius        
        if ((self._intersection[0]**2 + self._intersection[1]**2) 
        <= self._aprad**2):
            return self._intersection
                    
        else:
            self._intersection = None
            print "None."

    def refraction(self, incident, normal, n1, n2):
        """Calculates refracted ray with input of incident and normal vectors (as unit vectors) and the refractive indices n1 and n2 of the media."""
        
        cost1 = abs(np.inner(incident, normal))
        sint1 = abs(np.linalg.norm(np.cross(incident, normal)))
        
        #Case for total internal reflection
        if sint1 > (n2/n1):
            k2hat = None
            raise Exception("Total Internal Reflection")
            
        else:
            sint2 = (n1/n2)*sint1
            refracted = ((n1/n2)*incident + ((n1/n2)*cost1 - 
                                            (1-(sint2)**2)**0.5)*normal)
            k2hat = np.array(((1/np.linalg.norm(refracted)) * refracted))
            return k2hat
            
    def propagate_ray(self, ray):
        """Propagates a ray from its starting point to the lens"""
        
        kmag = ray._k / np.linalg.norm(ray._k)
        self.intercept(ray)
        
        if self._intersection == None:
            raise Exception("Ray Terminated; does not intersect with lens.")
        
        else:
            if self._curvature == 0:
                normal = np.array([0,0,1])
            
            elif self._curvature > 0:
                normal = self._intersection - self._centreofcurv
            
            else:
                normal = self._centreofcurv - self._intersection
        
        nhat = normal / np.linalg.norm(normal)
        
        newdirection = self.refraction(kmag, nhat, self._n1, self._n2)
        
        if newdirection == None:
            raise Exception("Invalid refracted ray direction")
        
        else:
            ray.append(self._intersection, newdirection)

class OutputPlane(OpticalElement):
    
    def __init__(self, z_intercept=0.0):
        self._zint = z_intercept
    
    def intercept(self, ray):
        """ Finds intersection point of refracted ray with z-axis."""
        
        zdiff = self._zint - ray._p[2]
        kmag = ray._k * (1/np.linalg.norm(ray._k))
        l = zdiff/kmag[2]
        self._intersection2 = np.array((ray._p + (l*kmag)))
        return self._intersection2
    
    def propagate_ray(self, ray):
        """ Propagates refracted ray to output plane."""
        
        self.intercept(ray)
        
        if self._intersection2 == None:
            return "Ray does not intersect with output plane."
        
        else:
            ray.append(self._intersection2, ray._k)