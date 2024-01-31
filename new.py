import cv2
import numpy as np
import mediapipe as mp
import random
import pymsgbox
#from playsound import playsound
from time import time, sleep
from PIL import ImageTk, ImageFont, ImageDraw, Image
import tkinter
import tkinter.ttk
import tkinter.messagebox

from mediapipe.tasks import python
from mediapipe.tasks.python import vision, BaseOptions
from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerOptions, HandLandmarker, HandLandmarkerOptions

root = tkinter.Tk()
cameraLabel = tkinter.Label(root)
cameraLabel.pack()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    _, frame = cap.read()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    img = ImageTk.PhotoImage(Image.fromarray(frame))
    cameraLabel.configure(image=img)
    cameraLabel.update()

root.mainloop()