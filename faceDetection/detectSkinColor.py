import imutils
import numpy as np
import argparse
import cv2

def onlyFace(img):
	lower = np.array([0, 30, 30], dtype = "uint8")
	upper = np.array([55, 255, 255], dtype = "uint8")

	# img = cv2.imread('../images/s1.jpg')
	# img = imutils.resize(img, width = 400)
	converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	skinMask = cv2.inRange(converted, lower, upper)
	skin = cv2.bitwise_and(img, img, mask = skinMask)
	return skin

# cv2.imshow("image1", img)
# cv2.imshow("image2", skin)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

