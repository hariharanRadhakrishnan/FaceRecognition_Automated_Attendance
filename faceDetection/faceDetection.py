import cv2

face_cascade = cv2.CascadeClassifier('F:\College\VII Sem\CV\FaceRecognition_Automated_Attendance\\faceDetection\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('F:\College\VII Sem\CV\FaceRecognition_Automated_Attendance\\faceDetection\haarcascade_eye.xml')

def getFaces(img):
    faces = face_cascade.detectMultiScale(img,1.1,7)
    cropped_faces = []
    for (x,y,w,h) in faces:
        roi_img = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_img)
        if(len(eyes)):
            cropped_faces.append(roi_img)
            # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    return cropped_faces