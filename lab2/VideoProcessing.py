#!/usr/bin/env python3

import numpy as np
import cv2
import imutils

import argparse
from time import sleep

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to video file.")
args = vars(ap.parse_args())

if not args.get("video"):
    print("Using FleaCam.")
    cap = cv2.VideoCapture(0)
else:
    print("Opening the following video: ", args.get("video"))
    cap = cv2.VideoCapture(args["video"])

sleep(1)
while True:
    _, frame = cap.read()                                           # Read image
    frame = imutils.resize(frame, height=400)                       # Resize image
    frame = frame[150:, :]
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)              # Convert bgr to hsv
    sat = cv2.extractChannel(hsv_image, 1)                          # Extract saturation channel
    _, thresh = cv2.threshold(sat, 75, 255, cv2.THRESH_BINARY)  # Binaryize image
    kernel = np.ones((3,3), np.uint8)
    erode = cv2.erode(thresh, kernel, iterations=15)
    dilate = cv2.dilate(erode, kernel, iterations=50)
    # Display image
    cv2.imshow("frame", erode)
    cv2.imshow("orig", frame)
    cv2.waitKey(15)
