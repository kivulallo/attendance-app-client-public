## Note:
**This was a school project where our team used a Raspberry Pi with a camera to recognize students to be able to log their attendance in class.
This is a proof-of-concept code and is only meant to be used for feature presentation.**

The client side runs on Raspberry Pi with Python 3, OpenCV 4.1.2 + Contrib. It can connect to Google Firestore database where the student names used to be stored, as well as to a MySQL database where the attendance database used to operate from.
The server side code that runs on a Linux-based server can be found [here](https://github.com/kivulallo/attendance-app-server-public).

## How it works:
#### Background task
* The client connects to the MQTT server installed on the server side.
* When a "training complete" notification comes from the server, it starts downloading the new trainer file with the fresh face data.
* When the download is complete, it will reload the face recognizer with the new file.

#### Face recognition
* When the camera sees a face, the code will try to recognize it.
* If the face is known, it will search for the associated name in Firestore to display it.
* When there is a known face, with name on the screen, the user has to confirm if the recognition is correct.
* If yes, the program will try to save attendance to the database, if the student has a lesson at the time.

## How to run:
```$ python3 run.py``` 
