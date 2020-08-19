import cv2
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from matplotlib import cm
import numpy as np
import printlog as pr
from firebase import firebasemanager

class UI:
    app = Tk()
    canvas = None

    mainFrame = Frame(app)
    mainFrame.place(x=0, y=0)
    lmain = Label(mainFrame)
    lmain.grid(row=0, column=0,columnspan=2)
    yesBtn = None
    noBtn = None
    fbm = None
    sqlm = None
    lbl = None
    buttonsDisabled = False
    defaultText = True
    main = None
    labelText = StringVar()

    def __init__(self,windowsize,title,main=None,mode=False):
        self.app.title(title)
        self.app.geometry(windowsize)
        self.labelText.set("Do you see your name on the screen?")
        self.lbl = Label(self.mainFrame,textvariable=self.labelText)
        self.defaultText = True
        self.lbl.configure(font=("Constantina",15))
        self.lbl.grid(row=1,column=0,columnspan=2)
        self.yesBtn = Button(self.mainFrame, text="YES", command=self.pressedYes)
        self.noBtn = Button(self.mainFrame, text="NO")
        self.yesBtn.grid(row=3,column=0)
        self.noBtn.grid(row=3,column=1)
        self.fbm = main.fr.fbm
        self.sqlm = main.fr.sqlm
        self.main = main

    def convert(self, numpyImage):
        return Image.fromarray(numpyImage)

    def disableButtons(self):
        self.yesBtn.config(state="disabled")
        self.noBtn.config(state="disabled")
        self.buttonsDisabled = True

    def enableButtons(self):
        self.yesBtn.config(state="normal")
        self.noBtn.config(state="normal")
        self.buttonsDisabled = False

    def pressedYes(self):
        pr.pl("pressed yes")
        self.sqlm.setAttended(self.main.fr.studentid,True)

    def pressedNo(self):
        pr.pl("pressed no")

    def writeAlreadyAttended(self):
        self.labelText.set("You have already marked this lesson attended.")
        self.defaultText = False
    def writeDefaultText(self):
        self.labelText.set("Do you see your name on the screen?")
        self.defaultText = True

    def writeText(self, text):
        self.labelText.set(text)
        self.defaultText = False
