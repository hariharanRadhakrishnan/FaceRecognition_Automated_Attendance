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

	names_list = []
	#For each landmark detected image , recognize it by using the csv database

	# gr = input("Is it a group image?:")
	gr=""
	for image in image_set:
		points,skew,laugh,img_shape = image
		img_data = [method,points,skew,laugh,img_shape]
		print("Skew:",skew,"\tLaugh:",laugh)
		start_time = time.time()
		names_list = recognize(img_data,gr)
		
		
			
		print("Recognized name: ",names_list)
		# print(names_list)

		# recognized_name.append([name,value])
		# print("\n",recognized_name[-1])
		# print("--- %s Seconds ---" % (time.time() - start_time))
		print()

	# Return the name of the recognized feature
	return names_list

def main_Individual(choice):

	while(choice.upper() == 'Y' or choice.upper() == 'YES'):
		os.system('cls')
		img = input("\nType test image name: ")
		img = cv2.imread('Data/images/Test/'+img+'.jpg')

		method = input("\n1.68 Point-Hausdroff Distance\n2.Feature Point Hausdroff Distance\n3.Feature Line Hausdroff Distance\n4.Vornoi LHD\n5.New Voronoi LHD\n6.Combined Vornoi LHD\n7.Hybrid Voronoi LHD\nChoose method of Recognition: \n:")
		names = []
		rec_name = main_common(img,method)
		

		choice = input("\nDo you want to test another image? Y/N: ")
		cv2.destroyAllWindows()

def main_All():
	count_correct =0
	count_incorrect =0
	method = input("\n1.68 Point-Hausdroff Distance\n2.Feature Point Hausdroff Distance\n3.Feature Line Hausdroff Distance\n4.Voronoi LHD\n5.New Voronoi LHD\n6.Combined Vornoi LHD\n7.Hybrid Voronoi LHD\nChoose method of Recognition: \n:")
	os.system('cls')
	for file in os.listdir('Data/images/Test'):
		if(file.endswith('.jpg')):
			name, ext = os.path.splitext(file)
			print("Running : ",file)
			img = cv2.imread(os.path.join("Data/images/Test",file))
			pr = ''
			name = name.split()
			rec_name = main_common(img,method)
			if(len(rec_name) == len(set(rec_name))):
				
				if(name[0] in rec_name[:2]):
					pr = 'Correct'
					count_correct+=1	
				else:
					pr = 'Wrong'
					count_incorrect+=1	
			else:
				if(name[0] in max(rec_name,key=rec_name.count) or name[0]==rec_name[0]):
					pr = 'Correct'
					count_correct+=1
				else:
					pr = 'Wrong'
					count_incorrect+=1
							
			print("Recognized name: ",rec_name,pr)
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
    
