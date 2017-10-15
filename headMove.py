import cv2
import imutils
import sys
import time
import Quartz



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
        Quartz.CFRelease(theEvent)


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


mouse = Mouse()
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.15)

    for (x, y, w, h) in face:
        cv2.circle(img, ((int)(x+w/2),(int)(y+h/2)), 3, (255,0,0), 2)
        mouse.move(x, y)


    cv2.circle(img,(650,450), 63, (0,0,255), 2)
    img = imutils.resize(img,500)
    cv2.imshow("image", img)

    k = cv2.waitKey(1) & 0xff
    if k == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
