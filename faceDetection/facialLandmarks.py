from imutils import face_utils
import dlib
import cv2

predictor = dlib.shape_predictor("F:\College\VII Sem\CV\FaceRecognition_Automated_Attendance\\faceDetection\shape_predictor_68_face_landmarks.dat")

def face_points(image):
    b,r = image.shape[:2]
    rect = dlib.rectangle(left=0,top=0,right=r,bottom=b)
    shape = predictor(image, rect)
    shape = face_utils.shape_to_np(shape)
    for (x, y) in shape:
        cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
    return image,shape