import numpy as np
import cv2


face_cascade = cv2.CascadeClassifier('res/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('res/haarcascade_eye.xml')

print("HI Welcome to project face detection")
number = input("enter 2 to detect face in a photo and 1 to detect face through webcam")
print (number)

if number == '1':
    print("sdf")
    cap = cv2.VideoCapture(0)
    while 1:
         ret, img = cap.read()
         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
         faces = face_cascade.detectMultiScale(gray, 1.15)
    
         for (x,y,w,h) in faces:
             cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
             roi_gray = gray[y:y+h, x:x+w]
             roi_color = img[y:y+h, x:x+w]
        
             eyes = eye_cascade.detectMultiScale(roi_gray)
             for (ex,ey,ew,eh) in eyes:
                 cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    
         cv2.imshow('img',img)
         k = cv2.waitKey(30) & 0xff
         if k == ord("q"):
            break
    
    cap.release()
    cv2.destroyAllWindows()

elif number == '2':
    img = cv2.imread('amogh.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
