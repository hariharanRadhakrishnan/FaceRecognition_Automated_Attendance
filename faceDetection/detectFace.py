import copy
import cv2
import imutils
from .Display import display
from .detectSkinColor import onlyFace

#Detect Faces
def detect(img):

    cropped_faces = []
    face_cascade = cv2.CascadeClassifier("C:/Users/sande/Desktop/CV/sandeep/Data/cascades/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier('C:/Users/sande/Desktop/CV/sandeep/Data/cascades/haarcascade_eye.xml')

    faces = face_cascade.detectMultiScale(img)
    for (x,y,w,h) in faces:
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_color)
        if(len(eyes)):
            cropped_faces.append(roi_color)
            cv2.rectangle(img,(x,y),(x+w,y+h+15),(255,0,0),2)
    # img = onlyFace(img)
    # display(img)
    return cropped_faces