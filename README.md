# Mousely

A Utility Application made with OpenCV allowing the user to control cursor with head movements and can perform click events using blinking of eyes. 

Blinking of left eye corresponds to Left click event.<br />
Blinking of right eye corresponds to Right click event.<br />
Blinking of both the eyes corresponds to Double click event.

Technology used : OpenCV, Quartz and Dlib 

Currently this application is compatible with OSX only.

## Dependencies Used

1. [Quartz](https://github.com/mayank408/Mousely/edit/master/README.md) : It is used to interact with the operating system and carry out events such as clicking and moving the cursor.

2. [Dlib](http://blog.dlib.net/2014/08/real-time-face-pose-estimation.html) : It is used to detect facial landmarks with high accuracy. Blinking detection in the project is done using this library.

3. [OpenCV](https://opencv.org) : It is the Computer vision library which has C/C++, Python, Java interfaces. For this project, I have used OpenCV in Python.



## Installation instructions for OSX

1. Installing Python3 using brew

```
brew install python3
```

2. Installing OpenCV

```
brew install opencv3
```

3. Installing Quartz
```
sudo pip3 install pyobjc-framework-Quartz
sudo pip3 install pyobjc-core
sudo pip3 install pyobjc
```

3. Installing Shape Predictor : Download http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

4. Installing Dlib : The complete instructions step by step for downloading dlib is given [here](https://www.learnopencv.com/install-dlib-on-macos/)

5. Installing Boost and Boost-Python (Required for dlib) : The complete instructions step by step for downloading boost and boost-python is given [here](https://www.pyimagesearch.com/2015/04/27/installing-boost-and-boost-python-on-osx-with-homebrew/)


## Running the app

Run eye_detection.py providing shape predictor as the argument.

```
python3 eye_detection.py -p res/shape_predictor_68_face_landmarks.dat 
```

## Screenshots

![](https://github.com/mayank408/Mousely/blob/master/img_demo/Screen%20Shot%202017-10-21%20at%206.19.26%20PM.png)

## Challenges / Todo

1. Improving Accuracy (obviously)
2. Distinguish more clearly between natural blinking of eyes and explicit blinking.
3. Compatibility with Windows.

## References

* https://www.pyimagesearch.com/2017/04/.../eye-blink-detection-opencv-python-dlib/

## License

```
MIT License

Copyright (c) 2017 Mayank Tripathi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```














