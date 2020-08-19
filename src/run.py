from face_recognizer import FaceRecognition
import cv2
from ui import UI
from PIL import Image, ImageTk
import mqttlistener
import printlog as pr


class Main:
    TRAINER_PATH = "../trainer/trainer.yml"
    CASCADE_PATH = "../haarcascades/haarcascade_frontalface_default.xml"
    FLIP_IMAGE = False
    cam = cv2.VideoCapture(0)
    fr = FaceRecognition(CASCADE_PATH, TRAINER_PATH, cam, FLIP_IMAGE)
    ui = None
    listener = mqttlistener.Listener()
    downloader = listener.downloader
    framecounter = 0
    lesson = 0

    def __init__(self, windowsize, title, mode=False):
        self.ui = UI(windowsize, title, self)

    def refresh(self):
        if self.downloader.downloadStarted:
            if self.downloader.downloadFinished:
                pr.pl("New trainer file downloaded, reloading")
                self.fr = None
                self.fr = FaceRecognition(self.CASCADE_PATH, self.TRAINER_PATH, self.cam, self.FLIP_IMAGE)
                pr.pl("Reloaded")
                self.downloader.downloadStarted = False
                self.downloader.downloadFinished = False
        ret, img = self.cam.read()
        img = self.fr.recognizeImg(img)
        toShow = ImageTk.PhotoImage(image=self.ui.convert(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
        self.ui.lmain.imgtk = toShow
        self.ui.lmain.configure(image=toShow)
        self.framecounter += 1
        if self.fr.isFacePresent:
            if not self.fr.studentid == 0:
                if self.framecounter > 30:
                    self.lesson = self.fr.sqlm.getCurrentLessonForStudent(self.fr.studentid)
                    self.framecounter = 0
                    pr.pl("student id : " + str(self.fr.studentid))
                else:
                    if self.lesson == 0: self.lesson = self.fr.sqlm.getCurrentLessonForStudent(self.fr.studentid)
                if self.lesson is not None:
                    if self.lesson[-1] == 1:
                        if not self.ui.buttonsDisabled: self.ui.disableButtons()
                        if self.ui.defaultText: self.ui.writeAlreadyAttended()
                    else:
                        if not self.ui.defaultText: self.ui.writeDefaultText()
                        if self.ui.buttonsDisabled: self.ui.enableButtons()
                else:
                    self.ui.writeText("You don't have lessons right now.")
                    if not self.ui.buttonsDisabled: self.ui.disableButtons()
            else:

                self.ui.writeText("I don't know you :(")
                if not self.ui.buttonsDisabled: self.ui.disableButtons()
        else:
            self.fr.fbm.lastid = 0
            self.lesson = 0
            if not self.ui.defaultText: self.ui.writeDefaultText()
            if not self.ui.buttonsDisabled: self.ui.disableButtons()
        k = cv2.waitKey(100)
        if k == 27:
            quit()
        self.ui.lmain.after(10, self.refresh)

    def main(self):
        try:
            self.ui.app.mainloop()
        except KeyboardInterrupt:
            quit()

    def startMqtt(self):
        self.listener.start()


if __name__ == "__main__":
    p = Main("640x550", "testcam")
    pr.pl("Starting MQTT")
    p.startMqtt()
    pr.pl("Started MQTT")
    p.refresh()
    pr.pl("Setting TKinter and OpenCV")
    pr.pl("Opening window")
    p.main()
    pr.pl("Exiting")
