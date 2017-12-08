import imutils
import dlib
import cv2
import copy
from imutils import face_utils
import numpy as np
import statistics

def getLEM(img,shape):
    print(shape[-1])
    for i,s in enumerate(shape):
        for i in range(1,len(s)):
            cv2.line(img,(s[i-1][0], s[i-1][1]),(s[i][0], s[i][1]),(0,0,255))
        cv2.line(img,(s[len(s)-1][0], s[len(s)-1][1]), (s[0][0], s[0][1]),(0,0,255))
    cv2.imshow("a",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_points(cropped_faces):

    features = []
    for i in cropped_faces:
        #Scale the image to needed size
        i = imutils.resize(i,width=650)                                

        #Detect all feature points(68) 
        shape_img,points,skew,laugh = face_points(i)          
        
        #Display image with points                     
        # cv2.imshow('img'+str(count),shape_img)  

        features.append([points,skew,laugh])
   
    return features


def detect_skew(left,right,center):
    left_ratio = abs(center-left)
    right_ratio = abs(center-right)

    diff = left_ratio - right_ratio
    # print("SKEW:",diff)
    if(abs(diff)<=35):
        return "straight"
    elif(diff>35):
        return "left"
    elif(diff<-35):
        return "right"

def detect_laugh(mouth):
    mouth = np.array(mouth)[:,1].tolist()
    median = statistics.median(mouth)
    smile = 0
    for i in mouth:
        if(abs(i-median) >=31.5):
            print(abs(i-median),end=" ")
            smile+=1
    if(smile>1):
        return "laugh"
    else:
        return "normal"


#Face points for one image only
def face_points(gray):
    predictor = dlib.shape_predictor("C:/Users/sande/Desktop/CV/sandeep/Data/Landmarks/shape_predictor_68_face_landmarks.dat")
    b,r = gray.shape[:2]
    rect = dlib.rectangle(left=0,top=0,right=r,bottom=b)
    points = predictor(gray, rect)
    points = face_utils.shape_to_np(points)
    shape=points
    face_curve = shape[:17]
    left_eyebro = shape[17:22]
    right_eyebro = shape[22:27]
    nose = shape[27:36]
    left_eye = shape[36:42]
    right_eye = shape[42:48]
    mouth = shape[48:68]
    # shape = [face_curve,left_eyebro,right_eyebro,nose,left_eye,right_eye,mouth]
    # getLEM(img,shape)
    
    skew = detect_skew(face_curve[1][0],face_curve[-1][0],nose[2][0])
    laugh = detect_laugh(mouth)
    for (x, y) in points:
        cv2.circle(gray, (x, y), 1, (0, 0, 255), -1)
    cv2.imshow("land",gray)
    cv2.waitKey(0)


        
    return gray,points.tolist(),skew,laugh