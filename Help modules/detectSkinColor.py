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

	converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# lower_low = np.array([0, 50, 50])
	# lower_high = np.array([10, 255, 255])
	# Mask1 = cv2.inRange(converted, lower_low, lower_high)


	# upper_low = np.array([170, 50, 50])
	# upper_high = np.array([180, 255, 255])
	# Mask2 = cv2.inRange(converted, upper_low, upper_high)

	# skinMask = cv2.add(Mask1,Mask2)
	# skinMask = cv2.bitwise_not(skinMask)

	lower = np.array([0, 0, 0], dtype = "uint8")
	upper = np.array([179, 150, 150], dtype = "uint8")
	skinMask = cv2.inRange(converted, lower, upper)

	im_floodfill = skinMask.copy()

	h, w = skinMask.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)

	cv2.floodFill(im_floodfill, mask, (0,0), 255);
	im_floodfill_inv = cv2.bitwise_not(im_floodfill)
	im_out = skinMask | im_floodfill_inv


	
	skin = cv2.bitwise_and(img, img, mask = im_out)
	return skin

