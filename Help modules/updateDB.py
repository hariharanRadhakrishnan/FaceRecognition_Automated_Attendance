import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH
from imutils import face_utils
import imutils
from detectSkinColor import onlyFace
import dlib
import cv2
import copy
import csv
import os
import statistics

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
    # print("Laugh:",end=" ")
    for i in mouth:
        # print(abs(i-median),end=" ")
        if(abs(i-median) >=31.5):
            smile+=1
    if(smile>1):
        return "laugh"
    else:
        return "normal"

#Face points for one image only
def face_points(gray):
    predictor = dlib.shape_predictor("facial-landmarks/shape_predictor_68_face_landmarks.dat")
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
    # for (x, y) in points:
    #     cv2.circle(gray, (x, y), 1, (0, 0, 255), -1)
    # cv2.imshow(".",gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()    

        
    return gray,points.tolist(),skew,laugh

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

    # count = 0
    # cv2.imshow('Detected Images',gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return cropped_faces

#For all detected images, store the (feature image,shape)
def get_points(cropped_faces):
    features = []
    count = 0
    for i in cropped_faces:
    	                                                                                    
        #Detect all feature points(68) 
        shape_img,points,skew,laugh = face_points(i)  

        #Display image with points           
        # cv2.imshow('img'+str(count),shape_img)                          
        # count += 1
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        
        features.append([points,skew,laugh])
   
    return features

#Write name and points into the csv table
def write_csv(name,points,filename):
    
    file =open('../Data/database/'+filename,'a+')
    file.write(name)
    for point in points:
        file.write(","+str(point[0])+" "+str(point[1]))
    file.write("\n")
    file.close()

#Process the image and take actions
def process(img,name):
	#Scale the image to needed size
	img = imutils.resize(img,width=800)
    
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#Detect thee faces in a picture
	cropped_faces = detect(img,gray)

	#Obtain points/andmarks for each detected face
	points_set = get_points(cropped_faces)
	# choice = input("update? Y/N: ")
	choice='Y'
	if(choice=='Y'):
		for points in points_set:
			point,skew,laugh = points
			#Input name and update points and name into a list into a file
			filename=''
			if(skew=="left"):
				filename="LEFT_DB.csv"
			elif(skew=="right"):
				filename="RIGHT_DB.csv"
			else:
				if(laugh=="laugh"):
					filename="LAUGH_DB.csv"
				else:
					filename="NORMAL_DB.csv"
			print(filename)
		write_csv(name,point,filename)
    

def main():
	count =0 
	for file in os.listdir('../Data/images/original'):
		print(file,end=" ")
		if(file.endswith('.jpg')):
			name, ext = os.path.splitext(file)
			img = cv2.imread(os.path.join("../Data/images/original",file))
			img = onlyFace(img)  
			process(img,name[:-4])


    
   
main()