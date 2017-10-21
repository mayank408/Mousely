# Mousely

A Utility Application made with OpenCV allowing the user to control cursor with head movements and can perform click event using 
blinking of eyes. 

Technology used : OpenCV, Quartz and Dlib 

Blinking of left eye corresponds to Left click event.<br />
Blinking of right eye corresponds to Right click event.<br />
Blinking of both the eyes corresponds to Double click event.

Currently this application is compatible with OSX only.

## Dependencies Used

1. [Quartz](https://github.com/mayank408/Mousely/edit/master/README.md) : It is used to interact with the operating system and carry out events such as clicking and moving the cursor.

2. [Dlib](http://blog.dlib.net/2014/08/real-time-face-pose-estimation.html) : It is used to detect facial landmarks with high accuracy. Blinking detection in the project is done using this library.

3. [OpenCV](https://opencv.org) : It is the Computer vision library which has C/C++, Python, Java interfaces. For this project, I have used OpenCV in Python.



## Installation instructions for OSX

1. Installing Python3 using brew

```
bew install python3
```

2. Installing OpenCV

```
bew install opencv3
```

3. Installing Shape Predictor : Download http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

4. Installing Dlib : The complete instructions step by step for downloading dlib is given [here](https://www.learnopencv.com/install-dlib-on-macos/)

5. Installing Boost and Boost-Python (Required for dlib) : The complete instructions step by step for downloading dlib is given [here](https://www.pyimagesearch.com/2015/04/27/installing-boost-and-boost-python-on-osx-with-homebrew/)


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
3. compatibility with Windows.

## References

* https://www.pyimagesearch.com/2017/04/.../eye-blink-detection-opencv-python-dlib/

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details














