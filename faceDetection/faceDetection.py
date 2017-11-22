import numpy as np
import tkinter as tk
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import copy

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

img = cv2.imread('../images/class10.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray,1.1,7)

cropped_faces = []
for (x,y,w,h) in faces:
    roi_color = copy.copy(img[y:y+h, x:x+w])
    roi_gray = copy.copy(gray[y:y+h, x:x+w])
    eyes = eye_cascade.detectMultiScale(roi_gray)
    if(len(eyes)):
        print(eyes)
        cropped_faces.append(roi_color)
        cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)

scale = 500
height, width = gray.shape[:2]
scale_factor = width/scale
scale_x = int(width/scale_factor)
scale_y = int(height/scale_factor)
count = 0
gray = cv2.resize(gray,(scale_x,scale_y))
cv2.imshow('Detected Images',gray)
cv2.waitKey(0)
cv2.destroyAllWindows()


scale = 200

for i in cropped_faces:
    height, width = i.shape[:2]
    scale_factor = width/scale
    scale_x = int(width/scale_factor)
    scale_y = int(height/scale_factor)
    i = cv2.resize(i,(scale_x,scale_y))
    cv2.imshow('img'+str(count),i)
    cv2.waitKey(0)
    count += 1

cv2.imshow('initail image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()