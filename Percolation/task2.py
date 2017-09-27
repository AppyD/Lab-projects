test1 = {'disks':[1,3,7,13], 'left':True, 'right':False}
test2 = {'disks':[14,17,2,22,3], 'left':False, 'right':False}

def joincluster(c1, c2):
    c1['disks'] = c1['disks'] + c2['disks']
    c1['disks'] = list(set(c1['disks']))
    if c1['left'] or c2['left']:
		c1['left'] = True
    if c1['right'] or c2['right']:
        c1['right'] = True
    print c1