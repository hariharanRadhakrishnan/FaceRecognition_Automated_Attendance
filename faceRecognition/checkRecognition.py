import sys
sys.path.insert(0, 'F:\College\VII Sem\CV\FaceRecognition_Automated_Attendance\\faceDetection')
import checkLHD as lhd
import faceDetection as fd
import facialLandmarks as fl
import cv2
import imutils

PATH = '../images/san.jpg'

image = cv2.imread(PATH)
# cv2.imshow("to be recognized",image)
# cv2.waitKey(0)

face_images = fd.getFaces(image)
# print(len(face_images))
output = 1
for i in face_images:
	i_copy = i.copy()
	i_copy = cv2.resize(i_copy,dsize = 200)
	i_copy, shape = fl.face_points(i_copy)
	print(list(shape))
	# cv2.namedWindow("window")
	# cv2.moveWindow("window",40,30)
	cv2.imshow(str(output),i_copy)
	cv2.waitKey(0)
	output += 1
	recognized, minmum = lhd.run(shape)
	for i in recognized:
		print(i)
	# if(minmum[0] < 5):
	print(output-1,minmum)
	# else:
		# print(output-1,"Not recognized")

# cv2.waitKey(0)