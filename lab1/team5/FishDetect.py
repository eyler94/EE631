#!/usr/bin/env python3

import numpy as np
import cv2 as cv
import argparse
from time import sleep

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to video file.")
ap.add_argument("-t", "--train", help="run the training program instead of using default values")
args = vars(ap.parse_args())

if not args.get("video"):
    print("Got no video path, using webcam.")
    cap = cv.VideoCapture(0)
else:
    print("Opening the following video: ", args.get("video"))
    cap = cv.VideoCapture(args["video"])

sleep(0.5)
while True:
    _, frame = cap.read()

    #####################
    # Work the video
    #####################
    _, frame1 = cap.read()
    if frame1 is None:
        break

    diff = cv.absdiff(frame,frame1)
    blur = cv.GaussianBlur(diff, (5,5), 0)
    erode = cv.erode(blur, None, iterations=5)
    dilate = cv.dilate(erode, None, iterations=20)

    frame = dilate
    #####################
    # Display the video
    #####################
    sleep(0.05)
    cv.imshow("Frame", frame)
    key = cv.waitKey(1) & 0xFF

    if key == ord("q"):
        break
