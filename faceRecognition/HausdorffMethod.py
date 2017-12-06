from .FeatureBuild import build_dlib_features
from .FeatureBuild import build_voronoi_features
from .PointHausdorff import point_hausdorff_distance
from .LineHausdorff import primaryLHD
from .LineHausdorff import convert
from .Voronoi import get_delaunay_lineset
import time

# #Convert 68 points into linesets for Line hausdorff distance
# def convert(s):
#     s = s.split(",")
#     s = [[int(x) for x in i.split()] for i in s]
#     lineSet = []
#     for i in range(1,len(s)):
#         lineSet.append([s[i-1],s[i]])
#     return lineSet

def hausdorff(test_points,temp_points,method,shape):
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
        
        distance = 0

        #Use the weightage for the classifiers here for each feature
        
        for i,feature in enumerate(features):
            distance +=  feature_weights[i]*point_hausdorff_distance(test_features[i],temp_features[i])
        

    #OPTION 3: Obtain features as a list and then find line hausdorff distance
    elif(method==3):
        temp_lineset = convert(temp_points)
        test_lineset = convert(test_points)
        # print(convert(test_points))

        #Calculate the Line hausdorff distance         
        distance = primaryLHD(test_lineset,temp_lineset)

    #OPTION 4: Obtain voronoi features as a list and find line hausdorff distance
    elif(method==4):
        temp_voronoi_features = get_delaunay_lineset(temp_points,shape[0],shape[1])
        test_voronoi_features = get_delaunay_lineset(test_points,shape[0],shape[1])

        # print("Test:")
        # print(test_voronoi_features)

        # print("\n\n\n")
        # print("Temp")
        # print(temp_voronoi_features)

        start_time = time.time()
        #Calculate the Line hausdorff distance
        distance = primaryLHD(temp_voronoi_features,test_voronoi_features)
        print("--- %s seconds ---" % (time.time() - start_time))

    return distance