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

if __name__ == '__main__':
    mouse = Mouse()
    if sys.platform == "darwin":
        print("Current mouse position: %d:%d" % mouse.position())
        print("Moving to 100:100...");
        mouse.move_rel(25, 16)
        print("Clicking 200:200 position with using the right button...");
        #mouse.click_pos(25, 16, 0)
        #mouse.click_pos(25, 16, 0)
        #mouse.click_pos(25, 16, 0)
        mouse.move(25, 26)
        time.sleep(0.05)
        mouse.move(35, 26)
        time.sleep(0.05)
        mouse.move(40, 26)
        time.sleep(0.05)
        mouse.move(44, 26)
        time.sleep(0.05)
        mouse.move(50, 26)
        time.sleep(0.05)
        mouse.move(55, 26)
        time.sleep(0.05)
        mouse.doubleClick(1264, 416, 2, 0)
        time.sleep(0.05)
        mouse.doubleClick(1264, 46, 2, 0)

        
        #mouse.doubleClick(25, 26, 2, 0)
    elif sys.platform == "win32":
        print("Error: Platform not supported!")

