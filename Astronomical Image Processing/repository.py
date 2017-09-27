def aperture(i, j):
    
    aperture_points = []
    index_reference = [(i,j), (i,j-1), (i,j-2),(i,j-3),(i,j-4),(i,j-5),
                       (i,j+1), (i,j+2), (i,j+3), (i,j+4), (i,j+5), (i,j+6),
                       (i-1,j-5), (i-1,j-4), (i-1,j-3), (i-1,j-2), (i-1,j-1), (i-1,j),
                       (i-1,j+1), (i-1,j+2), (i-1,j+3), (i-1,j+4), (i-1,j+5), (i-1,j+6), 
                       (i-2,j-4), (i-2,j-3), (i-2,j-2), (i-2,j-1), (i-2,j),
                       (i-2,j+1), (i-2,j+2), (i-2,j+3), (i-2,j+4), (i-2,j+5),
                       (i-3,j-3), (i-3,j-2), (i-3,j-1), (i-3,j),
                       (i-3,j+1), (i-3,j+2), (i-3,j+3), (i-3,j+4),
                       (i-4,j-2), (i-4,j-1), (i-4,j),
                       (i-4,j+1), (i-4,j+2), (i-4,j+3),
                       (i-5,j-1), (i-5,j),
                       (i-5,j+1), (i-5,j+2),
                       (i+1,j-5), (i+1,j-4), (i+1,j-3), (i+1,j-2), (i+1,j-1), (i+1,j),
                       (i+1,j+1), (i+1,j+2), (i+1,j+3), (i+1,j+4), (i+1,j+5), (i+1,j+6),
                       (i+2,j-5), (i+2,j-4), (i+2,j-3), (i+2,j-2), (i+2,j-1), (i+2,j),
                       (i+2,j+1), (i+2,j+2), (i+2,j+3), (i+2,j+4), (i+2,j+5), (i+2,j+6),
                       (i+3,j-4), (i+3,j-3), (i+3,j-2), (i+3,j-1), (i+3,j),
                       (i+3,j+1), (i+3,j+2), (i+3,j+3), (i+3,j+4), (i+3,j+5),
                       (i+4,j-3), (i+4,j-2), (i+4,j-1), (i+4,j),
                       (i+4,j+1), (i+4,j+2), (i+4,j+3), (i+4,j+4),
                       (i+5,j-2), (i+5,j-1), (i+5,j),
                       (i+5,j+1), (i+5,j+2), (i+5,j+3),
                       (i+6,j-1), (i+6,j),
                       (i+6,j+1), (i+6,j+2)]

    for k in index_reference:
        aperture_points.append(img_data[k])
    
    return aperture_points, index_reference