import copy
import cv2
import imutils
from .Display import display

def detect(img):
    #Detect Faces
    # img = imutils.resize(img,width=800)
    cropped_faces = []
    face_cascade = cv2.CascadeClassifier("C:/Users/sande/Desktop/CV/sandeep/Data/cascades/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier('C:/Users/sande/Desktop/CV/sandeep/Data/cascades/haarcascade_eye.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  

    faces = face_cascade.detectMultiScale(gray)
    for (x,y,w,h) in faces:
        roi_color = copy.copy(img[y-5:y+5+h+15, x-5:x+5+w])
        roi_gray = copy.copy(gray[y:y+h+15, x:x+w])
        eyes = []
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if(len(eyes)):
            cropped_faces.append(roi_color)
            cv2.rectangle(img,(x,y),(x+w,y+h+15),(255,0,0),2)
    img = imutils.resize(img,width=1000)
    display(img)
    return cropped_faces