import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH
from imutils import face_utils
import imutils
from detectSkinColor import onlyFace
import numpy as np
import dlib
import cv2
import copy





file = ''
# file = open("line_edge_maps.csv",'a')

def dist(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)*(1/2.0)
    # return dist_align(a,b)#+dist_scaled(a,b)+dist_tilted(a,b)+dist_skewed(a,b)


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

#Compute generic hausdrauff distance
def hausdroff_distance(set_a,set_b):
    # print()
    # print('ref_dist',ref_dist)
    
    #Calculate min from a -> b
    hausdrauff_dist_a = []
    for a in set_a:
        min_d = 9999
        for b in set_b:
            distance = dist(a,b)
            if(distance<min_d):
                min_d=distance
        hausdrauff_dist_a.append(min_d)
    # print("H A", max(hausdrauff_dist_a))
    #Calculate min from b -> a
    hausdrauff_dist_b = []
    for b in set_b:
        min_d = 9999
        for a in set_a:
            distance = dist(b,a) 
            if(min_d > distance):
                min_d=distance
        hausdrauff_dist_b.append(min_d)
    # print("H B", max(hausdrauff_dist_b))
    # print(max(hausdrauff_dist_a,hausdrauff_dist_b))
    return  max(max(hausdrauff_dist_a),max(hausdrauff_dist_b))

#Compute Hausdrauff distance for all points,and also shape specific
def hausdroff(test_points,temp_points):

    #OPTION 1: compute Hausdrauff distance for all points togethor
    return hausdroff_distance(test_points,temp_points)

    

    # #OPTION 2: compute Hausdrauff distance for individual shape feature and sum it, (add weightage later)
    # shapes = ['face_curve','left_eyebro','right_eyebro','nose','left_eye','right_eye','mouth']

    # temp_shape = build_shape(temp_points)
    # test_shape = build_shape(test_points)
    

    # #Use the weightage for the classifiers here for each feature
    # total = 0.075*hausdroff_distance(test_shape[0],temp_shape[0]) + 0.006*hausdroff_distance(test_shape[1],temp_shape[1]) + 0.006*hausdroff_distance(test_shape[2],temp_shape[2]) + 0.22*hausdroff_distance(test_shape[3],temp_shape[3]) + 0.13*hausdroff_distance(test_shape[4],temp_shape[4]) + 0.13*hausdroff_distance(test_shape[5],temp_shape[5]) + 0.2*hausdroff_distance(test_shape[6],temp_shape[6])
    # return total
    # return hausdroff_distance(test_shape[0],temp_shape[0])
    
    '''
    #OPTION 3: compute LEM and then do line hausdroff distance
    test_LEM = getLEM(test_shape)
    temp_LEM = getLEM(temp_shape)

    return line_hausdrauff_distance(test_LEM,temp_LEM)  

    '''

#Using the 68 landmark points identify the shape of the face
def build_shape(points):

    face_curve = points[:17]
    left_eyebro = points[17:22]
    right_eyebro = points[22:27]
    nose = points[27:36]
    left_eye = points[36:42]
    right_eye = points[42:48]
    mouth = points[48:]

    shape = [face_curve,left_eyebro,right_eyebro,nose,left_eye,right_eye,mouth]
    return shape
#Face points for one image only
def face_points(gray):
    predictor = dlib.shape_predictor("facial-landmarks/shape_predictor_68_face_landmarks.dat")
    b,r = gray.shape[:2]
    rect = dlib.rectangle(left=0,top=0,right=r,bottom=b)
    points = predictor(gray, rect)
    points = face_utils.shape_to_np(points)
    
    for (x, y) in points:
        cv2.circle(gray, (x, y), 1, (0, 0, 255), -1)

        
    return gray,points.tolist()

#Detect all images
def detect(img,gray):
    #Detect Faces
    cropped_faces = []
    face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')

    faces = face_cascade.detectMultiScale(gray)
    for (x,y,w,h) in faces:
        roi_color = copy.copy(img[y-5:y+5+h+15, x-5:x+5+w])
        roi_gray = copy.copy(gray[y:y+h+15, x:x+w])
        eyes = []
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if(len(eyes)):
            cropped_faces.append(roi_color)
            # cv2.rectangle(gray,(x,y),(x+w,y+h+15),(255,0,0),2)

    count = 0
    # cv2.imshow('Detected Images',gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return cropped_faces

#For all detected images, store the (feature image,shape)
def get_points(cropped_faces):

    features = []
    count = 0
    for i in cropped_faces:

        i = imutils.resize(i,width=200)                                #Scale the image to needed size

        
        shape_img,points = face_points(i)                               #Detect all feature points(68) 
        cv2.imshow('img'+str(count),shape_img)                          #Display image with points
        count += 1
        cv2.waitKey(0)

        
        
        features.append(points)
   
    return features
   
def mean_hausdroff(l):
    freq={}
    sum={}
    for x in l:
        if(x[1] in freq.keys()):
            freq[x[1]]+=1
            sum[x[1]]+=x[0]
        else:
            freq[x[1]]=1
            sum[x[1]]=x[0]
    result=[]
    for x in freq.keys():
        result.append([sum[x]/freq[x],x])
    return result

#Given a points set for a face, compute their hausdroff distance with all points set of faces in a DB and return the best match name
def recognize(test_points):
    hausdroff_list=[]

    #For each template in the database,compare test_feature
    #A template contains name and points corresponsding to it
    database = []
    with open("../images/easy/points yes-skin no-skew.csv") as f:
        lis=[line[:-1].split(',') for line in f] 
        
        for i in lis:
            name=i[0]
            points=i[1:]
            points=[[int(x) for x in p.split()] for p in points]
            # print(points)
            database.append([name,points])

    for template in database:
        #template[0] is name a, template[1] is 68 landmark points
        name,template_points = template
        hausdroff_list.append([hausdroff(template_points,test_points),name])

    #hausdroff_list is list of hausdroff values for each temple with the test image
    #Get the name,hausdrauff_dist for min with respect to first value in this list
    #Here value can either be Hausdroff distance of 1.All points togethor, 2. Weighted summation of each shape, 3.Line Hausdrauff Distance
    # # print()
    # 

    for i in range(len(hausdroff_list)-1,-1,-1):
        if(hausdroff_list[i][0]>=200):
            hausdroff_list.remove(hausdroff_list[i])
        
    for i in hausdroff_list:
        print(i)       
    
    print()
    hausdroff_list = mean_hausdroff(hausdroff_list)
   
    for i in hausdroff_list:
        print(i)

    value,name = min(hausdroff_list)
    # print()
    # print()
    threshold = 10000

    #If the min value is below a threshold only then return the name
    if(value<threshold):
        return name

    else:
        return "Not Found"
   
#LEM for one image only
def getLEM(shape,count):
    root = Tk()
    f = Frame()
    f.master.title("Lines "+str(count))
    f.pack(fill=BOTH, expand=1)
    canvas = Canvas(f)
    for s in shape:
        for i in range(1,len(s)):
            canvas.create_line(s[i-1][0], s[i-1][1], s[i][0], s[i][1])
        canvas.create_line(s[len(s)-1][0], s[len(s)-1][1], s[0][0], s[0][1])
    canvas.pack(fill=BOTH, expand=1)
    root.geometry("200x200+300+300")
    root.mainloop()

#Starting point: Main Function
def main(ip):
    img = cv2.imread('../images/Test/'+ip+'.jpg')
    #Detect/isolate image based on skin color
    img = onlyFace(img)                                                 
    img = imutils.resize(img,width=600)
    cv2.imshow("i",img)
    cv2.waitKey(0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    #Detect thee faces in a picture, Haar Cascade
    cropped_faces = detect(img,gray)

    #Obtain points/andmarks for each detected face, dlib facial landmarks
    points_set = get_points(cropped_faces)

    #For each detected and landmarked face, Do
    for points in points_set:
        #A points set is defined by 68 landmark points
        
        #Draw the LEM for the feature, recognize can be done inside
        #getLEM(shape, count)                                            

        #Recignize the feature from DB
        build_shape(points)
        # recognized_name = recognize(points)

        # #Display the name of the recognized feature
        # print(recognized_name)

    cv2.destroyAllWindows()

# main('Hari')
main('Boy')
# main('Girl')
# main('Josh')
# main('Nikhil')
# main('Nishanth')
# main('Parag')     #Accuracy not enough in 68 pts
# main('Pradeep')
# main('PratGM')
# main('Rachan')
# main('Rhea')
# main('Ritthwik')
# main('Sandeep')

