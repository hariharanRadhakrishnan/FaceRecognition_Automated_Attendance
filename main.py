import imutils
import cv2
import sys
from faceDetection.detectSkinColor import onlyFace
from faceDetection.detectFace import detect
from faceDetection.detectLandmarks import get_points
from faceRecognition.Recognize import recognize
import os

def main_common(img,method):
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

	#Detect the facial landmarks on the detected face using dlib data
	points_set = get_points(cropped_faces)

	recognized_name = "Not found"

	#For each landmark detected image , recognize it by using the csv database
	for points in points_set:
		recognized_name = recognize(points,method,img_shape)

	# Return the name of the recognized feature
	return recognized_name


def main_Individual(choice):

	while(choice.upper() == 'Y' or choice.upper() == 'YES'):
		os.system('cls')
		img = input("\nType test image name: ")
		img = cv2.imread('Data/images/Test/'+img+'.jpg')
		method = input("\n1.68 Point-Hausdroff Distance\n2.Feature Point Hausdroff Distance\n3.Feature Line Hausdroff Distance\n4.Vornoi Line Hausdroff Distance\nChoose method of Recognition: \n:")
		
		print("Recognized name: ",main_common(img,method))

		choice = input("\nDo you want to test another image? Y/N: ")
		cv2.destroyAllWindows()



def main_All():
	count_correct =0
	count_incorrect =0
	method = input("\n1.68 Point-Hausdroff Distance\n2.Feature Point Hausdroff Distance\n3.Feature Line Hausdroff Distance\n4.Verenoi Line Hausdroff Distance\nChoose method of Recognition: \n:")
	os.system('cls')
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
			print("Recognized name: ",rec_name)
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
		main_Individual(1)
	else:
		main_All()

if __name__ == "__main__":
	main()
    
