import numpy as np
import math
import matplotlib.pyplot as plt
from astropy.io import fits

def manual_mask(srow,erow,scol,ecol,image):
    ''' use to block remove parts of image manually e.g. stars
    row,scol = startrow,startcol; similarly for erow,ecol and end'''

    crow = srow   #current row
    ccol = scol   #current col
                                    
    for crow in range(srow,erow):
        for ccol in range(scol, ecol):
            image[crow][ccol] = 0
            ccol += 1
        crow += 1


def crap_removal(image):
    ''' Gets rid of known 'bad' areas on image.'''
    manual_mask(3000,3402,1227,1631,image)  # big central star  
    manual_mask(0,118,0,2570,image)         # edge
    manual_mask(4516,4611,0,2570,image)     # edge
    manual_mask(0,4611,0,122,image)         # edge
    manual_mask(0,4611,2472,2570,image)     # edge
    manual_mask(118,493,1289,1528,image)    # bottom horizontal spikes
    manual_mask(313,365,1019,1705,image)    # bottom horizontal spikes
    manual_mask(426,470,1100,1652,image)    # bottom horizontal spikes
    manual_mask(424,451,1027,1043,image)    # bottom horizontal spikes
    manual_mask(117,138,1526,1538,image)    # bottom horizontal spikes
    manual_mask(0,4611,1422,1450,image)     # vertical stripe
    manual_mask(3733,3788, 2107, 2161,image)    # bright star
    manual_mask(3708, 3803, 2129, 2137,image)     # bright star's spike
    manual_mask(3282, 3363, 735, 818,image)     # ditto for each pair below
    manual_mask(3202, 3419, 768, 784,image)
    manual_mask(2740, 2819, 938, 1009,image)
    manual_mask(2702, 2836, 967, 980,image)
    manual_mask(2253, 2320, 872, 942,image)
    manual_mask(2223, 2357, 901, 910,image)
    manual_mask(559, 596, 1755, 1794,image)
    manual_mask(1477, 1533, 616, 655,image)
    manual_mask(1400, 1452, 2061, 2117,image)
    manual_mask(2283, 2319, 428, 467,image)
    manual_mask(2286,2336, 2105,2156,image)
    manual_mask(2957, 3003, 1397, 1430,image)
    manual_mask(3385, 3441, 2441, 2499,image)
    manual_mask(3830, 3862, 2256, 2299,image)
    manual_mask(4012, 4052, 1437, 1481,image)
    manual_mask(4075, 4121, 532, 587,image)
    manual_mask(4317, 4346, 1347, 1385,image)
    manual_mask(4380, 4417, 1293, 1334,image)



################################################################################

def export_image(filename, image):
    hdu = fits.PrimaryHDU(image)
    hdu.writeto(filename)
    
'''    
def import_image(filename, image):
    new_file = fits.open(filename)
    global img_data
    image = new_file[0].data
'''

###############################################################################

def gaussian(mu, sigma, xvals=np.arange(3300,3600,0.01) ):
    ''' gaussian fit function with manual input to fit histogram'''
    
    norm = (1./(sigma*np.sqrt(2*np.pi)))
    gauss = []
    
    for x in xvals:
        main = np.exp( (-(x-mu)**2)/(2*sigma**2) )
        g = norm*main
        gauss.append(g)
    
    gmax = max(gauss)
    scale = (1.8e6)/gmax
    
    gaussians = [scale*i for i in gauss]
    
    return xvals, gaussians

###############################################################################

def find_index(flat_index):
    ''' takes flat index and returns true index in image'''
    
    num_cols = 2570      # number of columns in original image array
    j = flat_index
    i = 0
    
    while j > num_cols:
        j -= num_cols
        i += 1
            
    return i, j

###############################################################################

def find_max(image):
    '''finds max value in image'''
    
    intensities = image.flatten().tolist() #necessary to find max
    return max(intensities)

###############################################################################

def set_aperture(r, imax, jmax):

    aperture_coords = []
    
    for i in range(imax-r, imax+r+1):
        
        for j in range(jmax-r, jmax+r+1):
            
            if (np.abs(i-imax)**2 + np.abs(j-jmax)**2 <= r**2):
                
                aperture_coords.append((i,j))
    
    return aperture_coords

###############################################################################

def galaxy_background_sort(threshold, aperture_coords, image):     #threshold is 4 sigma of the background gaussian
    ''' sorts into 2 lists: background and source, also returns source coordinates as list. If not enough background in aperture, increases size and repeats'''

    ap_bkg = []                          # points in aperture that are background
    ap_galaxy = []                       # points in aperture that are part of the source
    galaxy_coords = []                   

    aperture_ints = [image[i] for i in aperture_coords]    # intensity at each coordinate
        
    ap_bkg = [y for y in aperture_ints if y < threshold]
    
    for i in xrange(0,len(aperture_ints)):                                   # sorts according to intensity
        if aperture_ints[i] > threshold:
            ap_galaxy.append(aperture_ints[i])
            galaxy_coords.append(aperture_coords[i])
    
    return ap_bkg, ap_galaxy, galaxy_coords

################################################################################
    
def galaxy_results(ap_bkg, ap_galaxy):    
    
        local_bkg = np.mean(ap_bkg)
        galaxy_list = [ap_galaxy[i] - local_bkg for i in range(len(ap_galaxy))]
        final_counts = np.sum(galaxy_list)
    
        tot_counts = np.sum(ap_galaxy)
        sig_bkg = 48                                # 4-sigma error from Gaussian (with sigma = 12)
        N = len(ap_galaxy)
        
        sig_counts = ( tot_counts + (N*sig_bkg)**2 )**0.5
        
        return final_counts, sig_counts, local_bkg
    
###############################################################################

def mask(points_list, image):
    for i in points_list:
        image[i] = 0
    print "masked!"

###############################################################################

def find_mag(final_counts, sig_counts):        # use final_counts for counts
    
    if final_counts < 0:
        raise Exception('Should not enter negative values into log function!')
    
    zp = 25.3
    zp_error = 0.02
    
    m = zp - 2.5*math.log(final_counts,10)
    m_err = ( (zp_error)**2 + ( (2.5*sig_counts) / (final_counts*math.log(10)) )**2 )**0.5
    
    return m, m_err

###############################################################################

def show_plot(image):
    plt.imshow(image, cmap='gray')

###############################################################################

### histogram of counts
''' type(img_data.flat)
    hist = plt.hist(img_data.flat, 1000) '''

### gaussian that fits the histogram!
'''
hist = plt.hist(list(img_data.flat), np.arange(3300,3600,5))
x,y = aimg.gaussian(3420, 12.)
plt.plot(x,y, label='Gaussian fit', linewidth=2.0)
plt.legend()
plt.xlabel('Pixel counts')
plt.ylabel('Number of pixels')
plt.title('Histogram of pixel counts in Mosaic image')
'''

#########



# Handing images from FITS files
# http://www.astropy.org/astropy-tutorials/FITS-images.html#Viewing-the-image-data-and-getting-basic-statistics