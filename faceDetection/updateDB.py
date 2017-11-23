import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH
from imutils import face_utils
import imutils
from detectSkinColor import onlyFace
import numpy as np
import dlib
import cv2
import copy
import csv
import os

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
        roi_color = copy.copy(img[y-5:y+5+h, x-5:x+5+w])
        roi_gray = copy.copy(gray[y:y+h, x:x+w])
        eyes = []
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if(len(eyes)):
            cropped_faces.append(roi_color)
            cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)

    count = 0
    cv2.imshow('Detected Images',gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return cropped_faces

#For all detected images, store the (feature image,shape)
def get_points(cropped_faces):

    features = []
    count = 0
    for i in cropped_faces:
    	#Scale the image to needed size
        i = imutils.resize(i,width=200)                                 

        #Detect/isolate image based on skin color
        i = onlyFace(i)                                                 

        #Detect all feature points(68) 
        shape_img,points = face_points(i)  

        #Display image with points           
        cv2.imshow('img'+str(count),shape_img)                          
        count += 1
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
        features.append(points)
   
    return features
   

def process(img,name):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Detect thee faces in a picture
    cropped_faces = detect(img,gray)

    #Obtain points/andmarks for each detected face
    points_set = get_points(cropped_faces)
    update_list=[]
    for points in points_set:
    	#Input name and update points and name into a list into a file
    	update_list.append((name,points))
    with open("data\points.csv","wb") as f:
        writer = csv.writer(f)
        print(update_list)
        writer.writerows(byte(update_list))


def main():
    for file in os.listdir('..\images\easy'):
        if(file.endswith('.jpg')):
            name=file[:-4]
            img = cv2.imread(os.path.join("..\images\easy",file))
            process(img,name)
	# path='../images/easy/img ('
	# for i in range(1,5):
	# 	full_path = path + str(i) +").jpg"
	# 	img = cv2.imread(full_path)
	# 	process(img)

main()