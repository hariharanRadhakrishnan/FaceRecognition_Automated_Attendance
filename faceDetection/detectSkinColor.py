import numpy as np
import cv2

def onlyFace(img):
# 	R > 95 and G > 40 and B > 20 and R > G and R > B
# and | R - G | > 15 and A > 15 and Cr > 135 and
# Cb > 85 and Y > 80 and Cr <= (1.5862*Cb)+20 and
# Cr>=(0.3448*Cb)+76.2069 and
# Cr >= (-4.5652*Cb)+234.5652 and
# Cr <= (-1.15*Cb)+301.75 and
# Cr <= (-2.2857*Cb)+432.85
# 0.0 <= H <= 50.0 and 0.23 <= S <= 0.68


	lower = np.array([0, 30, 30], dtype = "uint8")
	upper = np.array([55, 255, 255], dtype = "uint8")

	# lower = np.array([150, 10, 10], dtype = "uint8")
	# upper = np.array([220, 255, 255], dtype = "uint8")


	converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	skinMask = cv2.inRange(converted, lower, upper)
	skin = cv2.bitwise_and(img, img, mask = skinMask)
	
	return skin

