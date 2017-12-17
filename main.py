import imutils
import cv2
import sys
from faceDetection.detectSkinColor import onlyFace
from faceDetection.detectFace import detect
from faceDetection.detectLandmarks import get_img_data
from faceRecognition.Recognize import recognize
import os
from imutils import face_utils
import time


def main_common(img,method):

	recognized_name = []

	#Detect The face/s using facial and eye Haar cascades
	cropped_faces = detect(img)


	#Detect the facial landmarks on the detected face using dlib data
	image_set = get_img_data(cropped_faces)

	
	#For each landmark detected image , recognize it by using the csv database
	for image in image_set:
		points,skew,laugh,img_shape = image
		img_data = [method,points,skew,laugh,img_shape]
		print("Skew:",skew,"\tLaugh:",laugh,end="  ")
		start_time = time.time()
		recognized_name.append(recognize(img_data))
		print("--- %s Seconds ---" % (time.time() - start_time))

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
	method = input("\n1.68 Point-Hausdroff Distance\n2.Feature Point Hausdroff Distance\n3.Feature Line Hausdroff Distance\n4.Voronoi Line Hausdroff Distance\nChoose method of Recognition: \n:")
	os.system('cls')
	for file in os.listdir('Data/images/Test'):
		if(file.endswith('.jpg')):
			name, ext = os.path.splitext(file)
			print("Running : ",file)
			img = cv2.imread(os.path.join("Data/images/Test",file))
			rec_name = main_common(img,method)
			pr = ''
			if(name[:-4]==rec_name[0]):
				pr = 'Correct'
				count_correct+=1
			else:
				pr = 'Wrong'
				count_incorrect+=1
			print("Recognized name: ",rec_name[0],pr)
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
		main_Individual("Y")
	else:
		main_All()

if __name__ == "__main__":
	main()
    
