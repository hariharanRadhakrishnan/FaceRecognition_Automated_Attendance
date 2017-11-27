import imutils
import dlib
import cv2
import copy
from imutils import face_utils
import imutils


def get_points(cropped_faces):

    features = []
    count = 0
    for i in cropped_faces:
        #Scale the image to needed size
        i = imutils.resize(i,width=200)                                

        #Detect all feature points(68) 
        shape_img,points = face_points(i)          

        #Display image with points                     
        # cv2.imshow('img'+str(count),shape_img)  

        count += 1
       
        
        features.append(points)
   
    return features


#Face points for one image only
def face_points(gray):
    predictor = dlib.shape_predictor("C:/Users/sande/Desktop/CV/sandeep/Data/Landmarks/shape_predictor_68_face_landmarks.dat")
    b,r = gray.shape[:2]
    rect = dlib.rectangle(left=0,top=0,right=r,bottom=b)
    points = predictor(gray, rect)
    points = face_utils.shape_to_np(points)
    
    # for (x, y) in points:
    #     cv2.circle(gray, (x, y), 1, (0, 0, 255), -1)

        
    return gray,points.tolist()