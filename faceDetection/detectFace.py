import copy
import cv2
import imutils

def detect(img):
    #Detect Faces
    cropped_faces = []
    face_cascade = cv2.CascadeClassifier("C:/Users/sande/Desktop/CV/sandeep/Data/cascades/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier('C:/Users/sande/Desktop/CV/sandeep/Data/cascades/haarcascade_eye.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("skin-isolation",img)
    # cv2.waitKey(0)  

    faces = face_cascade.detectMultiScale(gray)
    for (x,y,w,h) in faces:
        roi_color = copy.copy(img[y-5:y+5+h+15, x-5:x+5+w])
        roi_gray = copy.copy(gray[y:y+h+15, x:x+w])
        eyes = []
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if(len(eyes)):
            cropped_faces.append(roi_color)
            cv2.rectangle(gray,(x,y),(x+w,y+h+15),(255,0,0),2)

    gray = imutils.resize(gray,width=800)
    count = 0
    cv2.imshow('Detected Images',gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return cropped_faces