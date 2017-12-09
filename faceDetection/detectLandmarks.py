import imutils
import dlib
import cv2
import copy
from imutils import face_utils
import numpy as np
import statistics
from .Display import display



#Detect if the face is skewed
def detect_skew(left,right,center):
    left_ratio = abs(center-left)
    right_ratio = abs(center-right)

    diff = left_ratio - right_ratio
    if(abs(diff)<=120):
        return "straight"
    elif(diff>120):
        return "left"
    elif(diff<-120):
        return "right"

#Detect if the face has a laugh
def detect_laugh(mouth):
    
    mouth = np.array(mouth)[:,1].tolist()
    median = statistics.median(mouth)
    smile = 0
    # print(max([abs(i-median) for i in mouth]))
    for i in mouth:
        if(abs(i-median) >=75):
            smile+=1
    if(smile>1):
        return "laugh"
    else:
        return "normal"

#Retrieve the 68 landmark points and skew,laugh
def get_img_data(cropped_faces):
    img_data = []
    for i in cropped_faces:

        #Scale the image to needed size
        i = imutils.resize(i,width=800)  

        #Detect all feature points(68) 
        points,skew,laugh = face_points(i)

        img_data.append([points,skew,laugh,i.shape])
   
    return img_data

#Face points for one image only
def face_points(gray):
    predictor = dlib.shape_predictor("C:/Users/sande/Desktop/CV/sandeep/Data/Landmarks/shape_predictor_68_face_landmarks.dat")
    b,r = gray.shape[:2]
    rect = dlib.rectangle(left=0,top=0,right=r,bottom=b)
    points = predictor(gray, rect)
    points = face_utils.shape_to_np(points)

    face_curve,left_eyebro,right_eyebro,nose,left_eye,right_eye,mouth = points[:17],points[17:22],points[22:27],points[27:36],points[36:42],points[42:48],points[48:68]
    
    skew = detect_skew(face_curve[1][0],face_curve[-1][0],nose[2][0])
    laugh = detect_laugh(mouth)

    for (x, y) in points:
        cv2.circle(gray, (x, y), 1, (0, 0, 255), -1)
    # scale = 500
    # height, width = gray.shape[:2]
    # scale_factor = width/scale
    # scale_x = int(width/scale_factor)
    # scale_y = int(height/scale_factor)
    # gray = imutils.resize(gray,(scale_x,scale_y))
    display(gray)
        
    return points.tolist(),skew,laugh