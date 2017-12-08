import imutils
import numpy as np
import argparse
import cv2

def onlyFace(img):
	lower = np.array([0, 48, 80], dtype = "uint8")
	upper = np.array([20, 255, 255], dtype = "uint8")

	# img = cv2.imread('../images/s1.jpg')
	# img = imutils.resize(img, width = 400)
	converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	skinMask = cv2.inRange(converted, lower, upper)
	k = skinMask
	# k = imutils.resize(k,width=1500)
	# cv2.imshow("",k)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
	# skinMask = cv2.erode(skinMask, kernel, iterations = 2)
	# skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
	# skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
	k = skinMask
	k = imutils.resize(k,width=1500)
	cv2.imshow("",k)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	skin = cv2.bitwise_and(img, img, mask = skinMask)
	return skin

img = cv2.imread("../../face_images/group1.jpg")
img = onlyFace(img)
img = imutils.resize(img,width=1500)
cv2.imshow("image1", img)
# cv2.imshow("image2", skin)
cv2.waitKey(0)
cv2.destroyAllWindows()