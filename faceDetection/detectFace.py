import copy
import cv2
import imutils
from .Display import display
from .detectSkinColor import onlyFace

#Detect Faces
def detect(img):

    # img = onlyFace(img)
    
    cropped_faces = []
    face_cascade = cv2.CascadeClassifier("C:/Users/sande/Desktop/CV/sandeep/Data/cascades/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier('C:/Users/sande/Desktop/CV/sandeep/Data/cascades/haarcascade_eye.xml')
    mouth_cascade = cv2.CascadeClassifier('C:/Users/sande/Desktop/CV/sandeep/Data/cascades/haarcascade_mcs_mouth.xml')
    faces = face_cascade.detectMultiScale(img,1.1,7)
    for (x,y,w,h) in faces:
        roi_color = img[y:y+h, x:x+w]
        roi_color = onlyFace(roi_color)
        eyes = eye_cascade.detectMultiScale(roi_color)
        mouth = mouth_cascade.detectMultiScale(roi_color)
        if(len(eyes) and len(mouth)):
            cropped_faces.append(roi_color)
            cv2.rectangle(img,(x,y),(x+w,y+h+15),(255,0,0),2)
    # display(img)
    return cropped_faces