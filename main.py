import imutils
import cv2
import sys
from faceDetection.detectSkinColor import onlyFace
from faceDetection.detectFace import detect
from faceDetection.detectLandmarks import get_points
from faceRecognition.Recognize import recognize

def main():
	choice = input("Do you want to test an image? Y/N : ")

	while(choice.upper() == 'Y' or choice.upper() == 'YES'):
		img = input("\nType test image name: ")
		img = cv2.imread('Data/images/Test/'+img+'.jpg')


	    #Detect/isolate image based on skin color
		img = onlyFace(img)         
		print("\n1.Check Skin Detection")

		#Resize the skin-isolated image                                        
		img = imutils.resize(img,width=600)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# cv2.imshow("skin-isolation",img)
		# cv2.waitKey(0)

		#Detect The face/s using facial and eye Haar cascades
		cropped_faces = detect(img,gray)
		print("\n2.Check Face Detection")


		#Detect the facial landmarks on the detected face using dlib data
		points_set = get_points(cropped_faces)
		print("\n3.Check Landmark Detection")


		#Choose method of recognition
		method = input("\n1.68 Point-Hausdroff Distance\n2.Feature Point Hausdroff Distance\n3.Feature Line Hausdroff Distance\n4.Verenoi Line Hausdroff Distance\nChoose method of Recognition:  ")


		#For each landmark detected image , recognize it by using the csv database
		for points in points_set:
			recognized_name = recognize(points,method)
			print("\n4.Check Face Recognition")
		# Display the name of the recognized feature
		print(recognized_name)

		choice = input("\nDo you want to test an test image? Y/N: ")
		cv2.destroyAllWindows()


    
main()
  
    