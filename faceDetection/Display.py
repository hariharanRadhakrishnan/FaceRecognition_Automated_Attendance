import cv2
import imutils

def display(img):
	img = imutils.resize(img,width=400)
	cv2.imshow("img",img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	pass