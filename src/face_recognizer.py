''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''
import cv2
import printlog as pr
from firebase import firebasemanager
from mysqlmanager import mysqlManager

class FaceRecognition:
    trainerPath = ''
    cascadePath = ''
    recognizer = None
    faceCascade = None
    font = cv2.FONT_HERSHEY_SIMPLEX
    cam = None
    useDatabase = False
    flipImage = False
    fbm = firebasemanager()
    sqlm = mysqlManager("host",3306,"user","password","db",fbm)
    studentid = 0

    id = 0
    minW = 0
    minH = 0

    isFacePresent = False

    ret,img = 0,0

    def __init__(self, cascadePath, trainerPath, cam, flipImage = False):
        pr.pl("OpenCV starting")
        self.cam = cam
        self.trainerPath = trainerPath
        self.cascadePath = cascadePath
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(self.trainerPath)
        self.faceCascade = cv2.CascadeClassifier(cascadePath)
        self.cam.set(3, 640)  # set video widht
        self.cam.set(4, 480)  # set video height
        # Define min window size to be recognized as a face
        self.minW = 0.1 * self.cam.get(3)
        self.minH = 0.1 * self.cam.get(4)
        self.flipImage = flipImage
        pr.pl("OpenCV started")


    def recognizeImg(self, img):
        if self.flipImage:
            img = cv2.flip(img, -1)  # Flip vertically

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(self.minW), int(self.minH)),
        )
        if len(faces) > 0:
            self.isFacePresent = True
        else:
            self.isFacePresent = False

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
            # Check if confidence is less them 100 ==> "0" is perfect match
            if (confidence < 75):
                self.studentid = id
                id = self.fbm.getNameForUserId(id)
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                self.studentid = 0
                confidence = "  {0}%".format(round(100 - confidence))
            cv2.putText(img, str(id), (x + 5, y - 5), self.font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), self.font, 1, (255, 255, 0), 1)

        return img

