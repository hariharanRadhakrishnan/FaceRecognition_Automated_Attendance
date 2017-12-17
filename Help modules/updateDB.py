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

#Detect all images
def detect(img):
    #Detect Faces
    cropped_faces = []
    face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY);
    faces = face_cascade.detectMultiScale(img,1.1,7)
    for (x,y,w,h) in faces:
        roi_color = copy.copy(img[y:y+h, x:x+w])
        roi_color=onlyFace(roi_color)
        eyes = eye_cascade.detectMultiScale(roi_color)
        if(len(eyes)):
            cropped_faces.append(roi_color)

    return cropped_faces

#Detect if the face is skewed
def detect_skew(left,right,center,img_size):
    # -89
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

#Face points for one image only
def face_points(img):
    predictor = dlib.shape_predictor("facial-landmarks/shape_predictor_68_face_landmarks.dat")
    b,r = img.shape[:2]
    rect = dlib.rectangle(left=0,top=0,right=r,bottom=b)
    points = predictor(img, rect)
    points = face_utils.shape_to_np(points)

    face_curve,left_eyebro,right_eyebro,nose,left_eye,right_eye,mouth = points[:17],points[17:22],points[22:27],points[27:36],points[36:42],points[42:48],points[48:68]
    
    skew = detect_skew(face_curve[1][0],face_curve[-1][0],nose[2][0],img.shape)
    laugh = detect_laugh(mouth,img.shape)
    
    for (x, y) in points:
        cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
    # cv2.imshow(str(skew)+" "+str(laugh),img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
        
    return points.tolist(),skew,laugh

#For all detected images, store the (feature image,shape)
def get_image_data(cropped_faces):
    img_data = []
    for i in cropped_faces:
    	        
        #Scale the image to needed size
        i = imutils.resize(i,width=200)

        #Detect all feature points(68) 
        points,skew,laugh = face_points(i)  

        
        img_data.append([points,skew,laugh,i.shape])
   
    return img_data

#Write name and points into the csv table
def write_csv(name,points,filename):
    
    file =open('../Data/database/'+filename,'a+')
    file.write(name)
    for point in points:
        file.write(","+str(point[0])+" "+str(point[1]))
    file.write("\n")
    file.close()

#Process the image and take actions
def process(img,name,file):
    
    filename=''

    # #Detect/isolate image based on skin color
    # img = onlyFace(img)


    #Detect The face/s using facial and eye Haar cascades
    cropped_faces = detect(img)


    #Detect the facial landmarks on the detected face using dlib data
    image_set = get_image_data(cropped_faces)


    for image in image_set:
        point,skew,laugh,img_shape = image

        if(skew=="left"):
            filename="LEFT_DB.csv"
            os.rename("C:/Users/sande/Desktop/CV/sandeep/Data/images/original/"+file, "C:/Users/sande/Desktop/CV/sandeep/Data/images/LEFT/"+file)
        elif(skew=="right"):
            os.rename("C:/Users/sande/Desktop/CV/sandeep/Data/images/original/"+file, "C:/Users/sande/Desktop/CV/sandeep/Data/images/RIGHT/"+file)
            filename="RIGHT_DB.csv"
        else:
            if(laugh=="laugh"):
                os.rename("C:/Users/sande/Desktop/CV/sandeep/Data/images/original/"+file, "C:/Users/sande/Desktop/CV/sandeep/Data/images/LAUGH/"+file)
                filename="LAUGH_DB.csv"
            else:
                os.rename("C:/Users/sande/Desktop/CV/sandeep/Data/images/original/"+file, "C:/Users/sande/Desktop/CV/sandeep/Data/images/NORMAL/"+file)
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
            		      
			process(img,name[:-4],file)
    
   
if __name__ == "__main__":
    main()