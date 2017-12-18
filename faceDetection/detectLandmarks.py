import imutils
import dlib
import cv2
import copy
from imutils import face_utils
import numpy as np
import statistics
from .Display import display
from .detectSkinColor import onlyFace



#Detect if the face is skewed
def detect_skew(left,right,center,img_size):
    left_ratio = abs(center-left)
    right_ratio = abs(center-right)

    diff = int((left_ratio - right_ratio)/img_size[0]*1000)
    if(abs(diff)<=150):
        return "straight"
    elif(diff>150):
        return "left"
    elif(diff<-150):
        return "right"

#Detect if the face has a laugh
def detect_laugh(mouth,img_size):
    
    mouth = np.array(mouth)[:,1].tolist()
    median = statistics.median(mouth)
    smile = 0
    m = [int(abs(i-median)/img_size[1]*1000) for i in mouth]

    for i in m:
        if(i >=100):
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
        # i = imutils.resize(i,width=200)

        height, width = i.shape[:2]

        # print(height,width,"\t",200, (200*height)/width)
        i = cv2.resize(i,(200, int((200*height)/width)),interpolation=cv2.INTER_CUBIC)
        #We use Interoplolation to resize
        # i = cv2.resize(i,(200, int((200*height)/width)),interpolation=cv2.INTER_LANCZOS4)
        
        #Detect all feature points(68) 
        i,points,skew,laugh = face_points(i)
        # i2,_,_,_ = face_points(i2)
        # display(i)
        img_data.append([points,skew,laugh,i.shape])
   
    return img_data

#Face points for one image only
def face_points(img):
    predictor = dlib.shape_predictor("C:/Users/sande/Desktop/CV/sandeep/Data/Landmarks/shape_predictor_68_face_landmarks.dat")
    b,r = img.shape[:2]
    rect = dlib.rectangle(left=0,top=0,right=r,bottom=b)
    points = predictor(img, rect)
    points = face_utils.shape_to_np(points)

    face_curve,left_eyebro,right_eyebro,nose,left_eye,right_eye,mouth = points[:17],points[17:22],points[22:27],points[27:36],points[36:42],points[42:48],points[48:68]
    
    skew = detect_skew(face_curve[1][0],face_curve[-1][0],nose[2][0],img.shape)
    laugh = detect_laugh(mouth,img.shape)

    for (x, y) in points:
        cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
    # img = onlyFace(img)
    
        
    return img,points.tolist(),skew,laugh