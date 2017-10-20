import cv2
import numpy as np

cap=cv2.VideoCapture(1)
fourcc=cv2.VideoWriter_fourcc(*'XVID')
out=cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))
while True:
	ret,frame=cap.read()
	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	out.write(frame)
	cv2.imshow('frame',frame)
	cv2.imshow('gray',gray)

	if waitKey(1) & OxFF == ord('q'):
		break

cap.release()
out.release()
cv2.destroyAllWindows()