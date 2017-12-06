import imutils
import cv2
import sys
from faceDetection.detectSkinColor import onlyFace
from faceDetection.detectFace import detect
from faceDetection.detectLandmarks import get_points
from faceRecognition.Recognize import recognize
import os

def main_common(img,method,display=0):
	#Detect/isolate image based on skin color
	img = onlyFace(img)         
	# print("\n1.Check Skin Detection")

	#Resize the skin-isolated image     
	if(method==1 or method==2):
		img = imutils.resize(img,width=200)    
	else:                               
		img = imutils.resize(img,width=800)

	img_shape=img.shape
	
	# cv2.imshow("skin-isolation",img)
	# cv2.waitKey(0)

	#Detect The face/s using facial and eye Haar cascades
	cropped_faces = detect(img)
	# print("\n2.Check Face Detection")


	#Detect the facial landmarks on the detected face using dlib data
	points_set = get_points(cropped_faces)
	# print("\n3.Check Landmark Detection")


	recognized_name = "Not found"
	#For each landmark detected image , recognize it by using the csv database
	for points in points_set:
		recognized_name = recognize(points,method,img_shape,display)
		# print("\n4.Check Face Recognition")
	# Display the name of the recognized feature
	return recognized_name


def main_Individual():
	choice = input("Do you want to test an image? Y/N : ")

	while(choice.upper() == 'Y' or choice.upper() == 'YES'):
		os.system('cls')
		img = input("\nType test image name: ")
		img = cv2.imread('Data/images/Test/'+img+'.jpg')
		# method = input("\n1.68 Point-Hausdroff Distance\n2.Feature Point Hausdroff Distance\n3.Feature Line Hausdroff Distance\n4.Verenoi Line Hausdroff Distance\nChoose method of Recognition: \n:")
		# print("Recognized method 1:",main_common(img,1,1))
		# print("Recognized method 2:",main_common(img,2))
		# print("Recognized method 3:",main_common(img,3,1))
		print("Recognized method 4:",main_common(img,4,1))

	    

		choice = input("\nDo you want to test an test image? Y/N: ")
		cv2.destroyAllWindows()





def main_All(method):
	count_correct =0
	count_incorrect =0
	for file in os.listdir('Data/images/Test'):
		if(file.endswith('.jpg')):
			name, ext = os.path.splitext(file)
			print("Running : ",file)
			img = cv2.imread(os.path.join("Data/images/Test",file))
			rec_name = main_common(img,method)
			if(name==rec_name):
				count_correct+=1
			else:
				count_incorrect+=1
			print("Recognized :",rec_name)
			print()
	print()
	print("CORRECT : ",count_correct)
	print("WRONG   : ",count_incorrect)

	accuracy = count_correct/float(count_correct+count_incorrect)
	accuracy = accuracy*100
	print("Accuracy:",accuracy,"%")
    
def main():
	print("1.Test Individual images:")
	print("2.Test all images")
	
	choice = int(input("Select your choice: "))
	print()
	if(choice==1):
		os.system('cls')
		main_Individual()
	else:
		# print("Method 1:")
		# main_All(1)
		# print("Method 2:")
		# main_All(2)
		print("Method 3:")
		main_All(3)
		# print("Method 4:")
		# main_All(4)

if __name__ == "__main__":
	main()
    
