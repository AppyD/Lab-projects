import astro_imaging as aimg
from astropy.io import fits
import numpy as np
import time

start = time.time()

mosaic = fits.open('mosaic.fits')
img_data = mosaic[0].data
bkg_global = 3420

aimg.crap_removal(img_data)
aperture_coords = aimg.set_aperture(254,3210,1434)
aimg.mask(aperture_coords, img_data)

threshold = 3468
max_intensity = max(img_data.flatten())
count = 0

f = open('galaxies_fixed_ap_full.txt', 'w')
f.write('Coordinates (x,y)\t')
f.write('Total Counts\t')
f.write('Count Error\t')
f.write('Magnitude\t')
f.write('Magnitude Error\t')
f.write('Local background\t')
f.write('Aperture radius (pixels)\n')

## loop things

while max_intensity > threshold:
    ap_rad = 6     # definition needs to be in the loop because we fiddle with the value of r
    
    flat_ind = np.argmax(img_data.flatten())
    
    imax, jmax = aimg.find_index(flat_ind)
    
    aperture_coords = aimg.set_aperture(ap_rad, imax, jmax)
  
    ap_bkg, ap_galaxy, galaxy_coords = aimg.galaxy_background_sort(threshold, aperture_coords, img_data)
        
    # mask the intensities if not enough points to qualify as a galaxy
    if len(ap_galaxy) < 20:
        aimg.mask(galaxy_coords, img_data)
        print "didn't qualify on size"
    
    else:
        
        # statistics
        final_counts, sig_counts, local_bkg = aimg.galaxy_results(ap_bkg, ap_galaxy)  
        
        # don't want negative magnitudes
        if final_counts > 0:
            
            count += 1
            mag, mag_error = aimg.find_mag(final_counts, sig_counts)
            
            f.write('('+str(imax)+','+str(jmax)+')' + '\t' + str(final_counts) + '\t' + str(sig_counts) + '\t'
                        + str(mag) + '\t' + str(mag_error) + '\t' +  str(local_bkg) + '\t' 
                        + str(ap_rad) + '\n') 

            print "Max Intensity: ", max_intensity
            print "Coordinates: ", imax, jmax
            print "Total Counts: ", final_counts
            print "Count Error: ", sig_counts
            print "Magnitude: ", mag
            print "Magnitude Error: ", mag_error
            print "Local bkg: ", local_bkg
            print "Aperture radius: ", ap_rad
            print count, " galaxies found so far!"
            
        else:
            print "didn't qualify on intensity."
        
        aimg.mask(galaxy_coords, img_data)
                    
    max_intensity = max(img_data.flatten())
    ap_bkg[:] = []          # clear lists to avoid appending issues
    ap_galaxy[:] = []
    galaxy_coords[:] = []
    aperture_coords[:] = []

f.close()

end = time.time()
print "Run time: ", (end-start)/60., " minutes."