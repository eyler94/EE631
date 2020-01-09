#!/usr/bin/env python3
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils

vs = VideoStream(0).start()
setting = "o" # ordinary

while True:
    if setting=="o":
        frame = vs.read()
        frame = imutils.resize(frame, width=600)
        cv2.imshow("Eyler", frame)
        key = cv2.waitKey(1) & 0xFF
    elif setting=="t":
        frame = vs.read()
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY_INV)[1]
        thresh = cv2.threshold(gray, 75, 255, cv2.THRESH_BINARY_INV)[1]
        cv2.imshow("Thresholding", thresh)
        key = cv2.waitKey(1) & 0xFF
    elif setting=="a":
        frame = vs.read()
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 30, 150)
        cv2.imshow("Canny (edge detection)", edge)
        key = cv2.waitKey(1) & 0xFF
    elif setting=="c":
        frame = vs.read()
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_f32 = np.float32(gray)
        corner = cv2.cornerHarris(gray, 2, 3, 0.04)
        corner = cv2.dilate(corner,None)
        corner[corner>0.01*corner.max()]=[0,0,255]
        cv2.imshow("Corner Detection", corner)
        key = cv2.waitKey(1) & 0xFF


    if key == ord("q"): # quit
        cv2.destroyAllWindows()
        break
    elif key== ord("o"): # ordinary
        cv2.destroyAllWindows()
        setting="o"
    elif key == ord("t"): # thresholding
        cv2.destroyAllWindows()
        setting="t"
    elif key == ord("a"): # Canny
        cv2.destroyAllWindows()
        setting="a"
    elif key == ord("c"): # Corner
        cv2.destroyAllWindows()
        setting="c"
