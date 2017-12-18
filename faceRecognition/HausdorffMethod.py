from .FeatureBuild import build_dlib_features
from .PointHausdorff import point_hausdorff_distance
from .NewLineHausdorff import newPrimaryLHD
from .NewLineHausdorff import primaryLHD
from .NewLineHausdorff import convert
from .Voronoi import get_delaunay_lineset
import time


def hausdorff(test_points,temp_points,method,shape,name,index):
    distance = 0
    method = int(method)

    #OPTION 1: compute Hausdrauff distance for all points togethor
    if(method==1):
        distance = point_hausdorff_distance(test_points,temp_points)

    #OPTION 2: compute Hausdrauff distance for individual shape feature and sum it, (add weightage later)
    elif(method==2):
        features = ['face_curve','left_eyebro','right_eyebro','nose','left_eye','right_eye','mouth']
        # ****Figure out the weights using a neural network****
        feature_weights = [0.075,0.006,0.006,0.22,0.13,0.13,0.2]

        temp_features = build_dlib_features(temp_points)
        test_features = build_dlib_features(test_points)
        
        distances = [feature_weights[i]*point_hausdorff_distance(test_features[i],temp_features[i])  for i,feature in enumerate(features)]
        distance = sum(distances)
        
    #OPTION 3: Obtain features as a list and then find line hausdorff distance
    elif(method==3):
        temp_lineset = convert(temp_points)
        test_lineset = convert(test_points)

        #Calculate the Line hausdorff distance         
        distance = newPrimaryLHD(test_lineset,temp_lineset)

    #OPTION 4: Obtain voronoi features as a list and find line hausdorff distance
    elif(method==4):
        temp_voronoi_features = get_delaunay_lineset(temp_points,shape[0],shape[1],name,index)
        test_voronoi_features = get_delaunay_lineset(test_points,shape[0],shape[1],name,index)
        distance = primaryLHD(temp_voronoi_features,test_voronoi_features)

    elif(method==5):
        temp_voronoi_features = get_delaunay_lineset(temp_points,shape[0],shape[1],name,index)
        test_voronoi_features = get_delaunay_lineset(test_points,shape[0],shape[1],name,index)
        distance = newPrimaryLHD(temp_voronoi_features,test_voronoi_features)

    elif(method==6):
        temp_voronoi_features = get_delaunay_lineset(temp_points,shape[0],shape[1],name,index)
        test_voronoi_features = get_delaunay_lineset(test_points,shape[0],shape[1],name,index)
        if(len(temp_voronoi_features)==len(test_points)):
            distance = newPrimaryLHD(temp_voronoi_features,test_voronoi_features)
        else:
            distance = primaryLHD(temp_voronoi_features,test_voronoi_features)

    return distance