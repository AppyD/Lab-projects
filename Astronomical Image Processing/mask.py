import matplotlib.pyplot as plt

def manual_mask(srow,erow,scol,ecol,show=1):
    '''row,scol = startrow,startcol; similarly for erow,ecol and end'''

    crow = srow   #current row
    ccol = scol   #current col
                                    
    for crow in range(srow,erow):
        for ccol in range(scol, ecol):
            aimg.img_data[crow][ccol] = 0
            ccol += 1
        crow += 1
    
    if show == 1:
        plt.imshow(aimg.img_data, cmap='gray')


def crap_removal():
    ''' Gets rid of known 'bad' areas on image.'''
    manual_mask(3000,3402,1227,1631,0)  # big central star  
    manual_mask(0,118,0,2570,0)         # edge
    manual_mask(4516,4611,0,2570,0)     # edge
    manual_mask(0,4611,0,122,0)         # edge
    manual_mask(0,4611,2472,2570,0)     # edge
    manual_mask(118,493,1289,1528,0)    # bottom horizontal spikes
    manual_mask(313,365,1019,1705,0)    # bottom horizontal spikes
    manual_mask(426,470,1100,1652,0)    # bottom horizontal spikes
    manual_mask(424,451,1027,1043,0)    # bottom horizontal spikes
    manual_mask(117,138,1526,1538,0)    # bottom horizontal spikes
    manual_mask(0,4611,1422,1450,0)     # vertical stripe
    manual_mask(3733,3788, 2107, 2161,0)    # bright star
    manual_mask(3708, 3803, 2129, 2137,0)     # bright star's spike
    manual_mask(3282, 3363, 735, 818,0)     # ditto for each pair below
    manual_mask(3202, 3419, 768, 784,0)
    manual_mask(2740, 2819, 938, 1009,0)
    manual_mask(2702, 2836, 967, 980,0)
    manual_mask(2253, 2320, 872, 942,0)
    manual_mask(2223, 2357, 901, 910,0)
    manual_mask(559, 596, 1755, 1794,0)
    manual_mask(1477, 1533, 616, 655,0)
    manual_mask(1400, 1452, 2061, 2117,0)
    manual_mask(2283, 2319, 428, 467,0)
    manual_mask(2286,2336, 2105,2156,0)
    manual_mask(2957, 3003, 1397, 1430,0)
    manual_mask(3385, 3441, 2441, 2499,0)
    manual_mask(3830, 3862, 2256, 2299,0)
    manual_mask(4012, 4052, 1437, 1481,0)
    manual_mask(4075, 4121, 532, 587,0)
    manual_mask(4317, 4346, 1347, 1385,0)
    manual_mask(4380, 4417, 1293, 1334,0)
