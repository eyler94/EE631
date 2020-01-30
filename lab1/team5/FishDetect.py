#!/usr/bin/env python3

import numpy as np
import cv2 as cv
import argparse
from time import sleep
from Flea2Camera import FleaCam

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to video file.")
args = vars(ap.parse_args())


if not args.get("video"):
    print("Using FleaCam.")
    from Flea2Camera import FleaCam
    cap = FleaCam()
else:
    print("Opening the following video: ", args.get("video"))
    cap = cv.VideoCapture(args["video"])




sleep(1)
print("q: quit\np: pause")
while True:
    #_, frame0 = cap.read()
    frame0 = cap.getFrame()
    #####################
    # Work the video
    #####################
    #_, frame1 = cap.read()
    frame1 = cap.getFrame()
    if frame1 is None:
        break

    diff = cv.absdiff(frame0,frame1)
    blur = cv.GaussianBlur(diff, (5,5), 0)
    erode = cv.erode(blur, None, iterations=5)
    dilate = cv.dilate(erode, None, iterations=10)

    frame = dilate
    b,g,r = cv.split(frame)
    print("Blue max:", np.max(b))
    print("Green max:", np.max(g))
    print("Red max:", np.max(r))
    # b_max = np.max(np.uint32(b))
    # g_max = np.max(np.uint32(g))
    # r_max = np.max(np.uint32(r))
    #
    # cv.putText(frame0, caption, (10,50), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)


    #####################
    # Display the video
    #####################
    sleep(0.1)
    cv.imshow("Frame0", frame0)
    cv.imshow("Frameb", b)
    cv.imshow("Frameg", g)
    cv.imshow("Framer", r)


    key = cv.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord("p"):
        print("Blue max:", np.max(b))
        print("Green max:", np.max(g))
        print("Red max:", np.max(r))
        _ = input("Press the anykey to continue.")
