# -*- coding: utf-8 -*-
"""
**************************************************************************
*                  Cross_A_Crater (e-Yantra 2016)
*                  ================================
*  This software is intended to teach image processing concepts
*
*  MODULE: Task2
*  Filename: hsvtrackbar.py
*  Version: 2.0.0  
*  Date: February 23, 2017
*  
*  Author: Jayant Solanki, e-Yantra Project, Department of Computer Science
*  and Engineering, Indian Institute of Technology Bombay.
*  
*  Software released under Creative Commons CC BY-NC-SA
*
*  For legal information refer to:
*        http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode 
*     
*
*  This software is made available on an “AS IS WHERE IS BASIS”. 
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using 
*  ICT(NMEICT)
*
**************************************************************************
"""
#This python code will help you to quickly arrive at the np arrays for hsv masking of the object of interest
import cv2
import numpy as np
import time

def nothing(x):
    pass

# Create a black image, a window
cap = cv2.VideoCapture(0)
time.sleep(5)
cv2.namedWindow('image', flags=1)

# create trackbars for color change
cv2.createTrackbar('Mn1','image',0,179,nothing)
cv2.createTrackbar('Mn2','image',0,255,nothing)
cv2.createTrackbar('Mn3','image',0,255,nothing)
cv2.createTrackbar('Mx1','image',0,179,nothing)
cv2.createTrackbar('Mx2','image',0,255,nothing)
cv2.createTrackbar('Mx3','image',0,255,nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)
while(1):
    
    ret, img = cap.read()
    # img = cv2.imread("test.jpg")
    # rotating image
    # rows,cols,l = img.shape
    # M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    # img = cv2.warpAffine(img,M,(cols,rows))
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # hsv=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    Mn1 = cv2.getTrackbarPos('Mn1','image')
    Mn2 = cv2.getTrackbarPos('Mn2','image')
    Mn3 = cv2.getTrackbarPos('Mn3','image')
    Mx1 = cv2.getTrackbarPos('Mx1','image')
    Mx2 = cv2.getTrackbarPos('Mx2','image')
    Mx3 = cv2.getTrackbarPos('Mx3','image')
    s = cv2.getTrackbarPos(switch,'image')

    if s == 0:
        img[:] = img
    else:
        lower=np.array([Mn1,Mn2,Mn3])
        upper=np.array([Mx1,Mx2,Mx3])
        # img=cv2.inRange(hsv,lower,upper)
        # lower = numpy.array([0, 0, 0]) #black color mask
        # upper = numpy.array([120, 120, 120])
        mask = cv2.inRange(hsv, lower, upper)
        # img = cv2.inRange(hsv, lower, upper)
        img=cv2.bitwise_and(img,img,mask=mask)
    cv2.imshow('images',img)

cv2.destroyAllWindows()