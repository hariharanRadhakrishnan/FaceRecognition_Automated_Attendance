#Compute generic hausdrauff distance
def point_hausdorff_distance(set_a,set_b):
    #Calculate min from a -> b
    point_hausdorff_distance_a = []
    for a in set_a:
        min_d = 9999
        for b in set_b:
            distance = dist(a,b)
            if(distance<min_d):
                min_d=distance
        point_hausdorff_distance_a.append(min_d)

    #Calculate min from b -> a
    point_hausdorff_distance_b = []
    for b in set_b:
        min_d = 9999
        for a in set_a:
            distance = dist(b,a) 
            if(min_d > distance):
                min_d=distance
        point_hausdorff_distance_b.append(min_d)

    return  max(max(point_hausdorff_distance_a),max(point_hausdorff_distance_b))



#This is the overall calculated distance measure
def dist(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)*(1/2.0)
    # return dist_align(a,b)+dist_scaled(a,b)+dist_tilted(a,b)+dist_skewed(a,b)

#This is the distance measure adjusted to a frame of reference for scaled image
def dist_scaled(a,b):
    ref_a = a[int(len(a)/2)]
    ref_b = b[int(len(b)/2)]
    new_a = ( (a[0]-ref_a[0])**2 + (a[1]-ref_a[1])**2)*(1/2.0)
    new_b = ( (b[0]-ref_b[0])**2 + (b[1]-ref_b[1])**2)*(1/2.0)

    return abs(new_a-new_b)

#This is the distance measure adjusted to a frame of reference for tilted image
def dist_tilted(a,b):
    pass
#This is the distance measure adjusted to a frame of reference for skewed image
def dist_skewed(a,b):
    pass

