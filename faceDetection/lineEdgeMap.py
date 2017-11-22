import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import copy

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

img = cv2.imread('../images/image9.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.2, 5)

def dist(a,b):
    return ( (a[0]-b[0])**2 + (a[1]-b[1])**2)*(1/2.0)

def hausdroff_distance(set_a,set_b):
    hausdrauff_dist_a = 0
    hausdrauff_pts_a=[]
    for a in set_a:
        min_d = 9999
        min_pts = []
        for b in set_b:
            distance = dist(a,b)
            if(distance<min_d):
                min_d=distance
                min_pts=a,b
        if(min_d>hausdrauff_dist_a):
            hausdrauff_dist_a=min_d
            hausdrauff_pts_a=min_pts

    hausdrauff_dist_b = 0
    hausdrauff_pts_b=[]
    for b in set_b:
        min_d = 9999
        min_pts = []
        for a in set_a:
            distance = dist(b,a)
            if(distance<min_d):
                min_d=distance
                min_pts=b,a
        if(min_d>hausdrauff_dist_b):
            hausdrauff_dist_b=min_d
            hausdrauff_pts_b=min_pts

    return  [hausdrauff_dist_a,hausdrauff_dist_b] #,  hausdrauff_pts_a,hausdrauff_pts_b 

def hausdroff(img_features,temp_features):
    features = ['face_curve','left_eyebro','right_eyebro','nose','left_eye','right_eye','mouth']
    total = 0
    for i,feature in features:
        #Use the weightage for the classifiers here for each feature
        total += hausdroff_distance(img_features[i],temp_features[i])
    return total

def recognize(img_features):
    threshold = ?
    min_d = 9999
    index = 0
    for i,temp_features in enumerate(each_template_from_db):
        dist = hausdroff(img_features, temp_features)
        if(dist < min_d):
            min_d = dist
            index = i
    if(min_d < threshold):
        return index
    else:
        return -1

def face_points(gray):
    b,r = gray.shape[:2]
    rect = dlib.rectangle(left=0,top=0,right=r,bottom=b)
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)
    face_curve = shape[:17]
    left_eyebro = shape[17:22]
    right_eyebro = shape[22:27]
    nose = shape[27:36]
    left_eye = shape[36:42]
    right_eye = shape[42:48]
    mouth = shape[48:]
    for (x, y) in shape:
        cv2.circle(gray, (x, y), 1, (0, 0, 255), -1)
    return gray,[face_curve,left_eyebro,right_eyebro,nose,left_eye,right_eye,mouth]

def getLEM(shape,count):
    features = ['face_curve','left_eyebro','right_eyebro','nose','left_eye','right_eye','mouth']
    root = Tk()
    f = Frame()
    f.master.title("Lines "+str(count))
    f.pack(fill=BOTH, expand=1)
    canvas = Canvas(f)
    for j,s in enumerate(shape):
        #print()
        #print(features[j],len(s))
        for i in range(1,len(s)):
            #print('(',s[i-1][0], s[i-1][1],')','(', s[i][0], s[i][1],')')
            canvas.create_line(s[i-1][0], s[i-1][1], s[i][0], s[i][1])
    canvas.pack(fill=BOTH, expand=1)
    root.geometry("200x200+300+300")
    root.mainloop()

def main():
    cropped_faces = []
    for (x,y,w,h) in faces:
        roi_color = copy.copy(img[y-5:y+5+h, x-5:x+5+w])
        cropped_faces.append(roi_color)
        cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)


    count = 0
    #cv2.imshow('Detected Images',gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    scale = 200

    for i in cropped_faces:
        height, width = i.shape[:2]
        scale_factor = width/scale
        scale_x = int(width/scale_factor)
        scale_y = int(height/scale_factor)
        i = cv2.resize(i,(scale_x,scale_y))
        i,features = face_points(i)
        cv2.imshow('img'+str(count),i)

        index = recognize(features)

        print(database[index])
        #getLEM(shape, count)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        count += 1

main()