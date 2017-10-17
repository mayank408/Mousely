from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import sched, time
import time
import sys
import time
import Quartz
import math
from datetime import datetime, date


now = time.time()

class Mouse():
    down = [Quartz.kCGEventLeftMouseDown, Quartz.kCGEventRightMouseDown, Quartz.kCGEventOtherMouseDown]
    up = [Quartz.kCGEventLeftMouseUp, Quartz.kCGEventRightMouseUp, Quartz.kCGEventOtherMouseUp]
    [LEFT, RIGHT, OTHER] = [0, 1, 2]

    def position(self):
        point = Quartz.CGEventGetLocation( Quartz.CGEventCreate(None) )
        return point.x, point.y

    def __mouse_event(self, type, x, y):
        mouse_event = Quartz.CGEventCreateMouseEvent(None, type, (x, y), Quartz.kCGMouseButtonLeft)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouse_event)

    def move(self, x, y):
        self.__mouse_event(Quartz.kCGEventMouseMoved, x, y)
        Quartz.CGWarpMouseCursorPosition((x, y))

    def press(self, x, y, button=0):
        event = Quartz.CGEventCreateMouseEvent(None, Mouse.down[button], (x, y), button)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

    def release(self, x, y, button=0):
        event = Quartz.CGEventCreateMouseEvent(None, Mouse.up[button], (x, y), button)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

    def doubleClick(self, x, y, clickCount, button=0):
        print("Double click event")
        theEvent = Quartz.CGEventCreateMouseEvent(None, Mouse.down[button], (x, y), button)
        Quartz.CGEventSetIntegerValueField(theEvent, Quartz.kCGMouseEventClickState, clickCount)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)
        Quartz.CGEventSetType(theEvent, Quartz.kCGEventLeftMouseUp)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)
        Quartz.CGEventSetType(theEvent, Quartz.kCGEventLeftMouseDown)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)
        Quartz.CGEventSetType(theEvent, Quartz.kCGEventLeftMouseUp)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)
        print("Double click event ended")


    def click(self, button=0):
        x, y = self.position()
        self.press(x, y, button)
        self.release(x, y, button)

    def click_pos(self, x, y, button=0):
        self.move(x, y)
        self.click(button)

    def torelative(self, x, y):
        curr_pos = Quartz.CGEventGetLocation( Quartz.CGEventCreate(None) )
        x += curr_pos.x;
        y += curr_pos.y;
        return [x, y]

    def move_rel(self, x, y):
        [x, y] = self.torelative(x, y)
        moveEvent = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, Quartz.CGPointMake(x, y), 0)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, moveEvent)

    def mouseEvent(self, type, posx, posy):
        theEvent = Quartz.CGEventCreateMouseEvent(None, type, (posx,posy), Quartz.kCGMouseButtonLeft)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)

    def mousedrag(self, posx, posy):
        self.mouseEvent(Quartz.kCGEventLeftMouseDragged, posx,posy)




def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")
ap.add_argument("-i", "--image", required=True,
    help="path to input image")
# ap.add_argument("-v", "--video", type=str, default="",
#                 help="path to input video file")
args = vars(ap.parse_args())

# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3

# initialize the frame counters and the total number of blinks
COUNTER = 0
TOTAL = 0

s = sched.scheduler(time.time, time.sleep)


def print_time():
    if ear > .3:
        COUNTER = 0

def print_some_times():
    print (time.time())
    s.enter(1, 1, print_time, ())
    s.run()
    print (time.time())


# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")
# vs = FileVideoStream(args["video"]).start()
# fileStream = True
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
fileStream = False
time.sleep(1.0)
currentCount = 0
# loop over frames from the video stream

mouse = Mouse()
face_cascade = cv2.CascadeClassifier('res/haarcascade_frontalface_default.xml')

while True:

    # if this is a file video stream, then we need to check if
    # there any more frames left in the buffer to process
    if fileStream and not vs.more():
        break

    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale
    # channels)
    frame = vs.read()
    frame = imutils.resize(frame, width=450)

    width, height, c = frame.shape

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.circle(frame, ((int)(height/2),(int)(width/2)), 4, (0,0,255), 2)
    cv2.circle(frame, ((int)(height/2),(int)(width/2)), 25, (128,0,128), 2)
    face = face_cascade.detectMultiScale(gray, 1.15)

    

    for (x, y, w, h) in face:
        slope = math.atan((float)((y+h/2 - height/2)/(y+h/2 - width/2)))
        #print (slope)
        cv2.circle(frame, ((int)(x+w/2), (int)(y+h/2)), 3, (255,0,0), 2)
        d = dist.euclidean((x+w/2, y+h/2), (width/2, height/2))
        c, e = mouse.position()
        if(d>25):
            t = time.time()
            while (time.time() - t < 2):
                j = dist.euclidean((x+w/2, y+h/2), (width/2, height/2)) 
                print (j)
                mouse.move(x + w/2 + math.sin(slope)*100*(time.time() - t), y + h/2 + math.cos(slope)*100*(time.time() - t))
                if(j<25):
                    break 
 
    # detect faces in the grayscale frame
    rects = detector(gray, 0)
    prevcount = 0
    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)


        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0

        # if ear > .42 or COUNTER > 5:
        # 	print(ear)
        # 	TOTAL = 0
        # compute the convex hull for the left and right eye, then
        # visualize each of the eyes

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull],  -1, (0, 255, 0), 1)

        # check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter
        
        if leftEAR < EYE_AR_THRESH - 0.12 and rightEAR > EYE_AR_THRESH - 0.12:
            print ("Left Eye Blinked")
            m,n = mouse.position()
            mouse.click_pos(m, n, 0)
            time.sleep(1)

        elif rightEAR < EYE_AR_THRESH - 0.12 and leftEAR > EYE_AR_THRESH - 0.12:
            print ("Right Eye Blinked")  
            m,n = mouse.position()
            mouse.click_pos(m, n, 1)
            time.sleep(1) 

        if (leftEAR < EYE_AR_THRESH - 0.12 and rightEAR < EYE_AR_THRESH - 0.12):
            print("Both Eyes Blinked")
            m,n = mouse.position()
            mouse.doubleClick(m, n, 2, 0)
            COUNTER += 1
            TOTAL += 1    
            prevcount = COUNTER
            time.sleep(1)

        # Mouse.doubleClick(1264, 416, 2, 0)
        

        # the computed eye aspect ratio for the frame
        cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Left: {}".format(leftEAR), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Right: {}".format(rightEAR), (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()

