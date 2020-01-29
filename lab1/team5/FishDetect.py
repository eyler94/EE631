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

sleep(1)
print("q: quit")#\np: pause")
# b_total = 0
# g_total = 0
# r_total = 0
# counter = 0
sum0 = 0
sum1 = 0
sum2 = 0
sum3 = 0
sum4 = 0
while True:
    _, frame0 = cap.read()

    #####################
    # Work the video
    #####################
    _, frame1 = cap.read()
    if frame1 is None:
        break

    diff = cv.absdiff(frame0,frame1)
    blur = cv.GaussianBlur(diff, (5,5), 0)
    erode = cv.erode(blur, None, iterations=5)
    dilate = cv.dilate(erode, None, iterations=10)

    frame = dilate
    b,g,r = cv.split(frame)
    b_max = np.max(np.uint32(b))
    g_max = np.max(np.uint32(g))
    r_max = np.max(np.uint32(r))

    # b_total += b_max
    # g_total += g_max
    # r_total += r_max
    # counter+=1
    # sum_max = b_max+g_max+r_max
    sum4 = sum3
    sum3 = sum2
    sum2 = sum1
    sum1 = sum0
    sum0 = b_max+g_max+r_max

    # sum_avg = np.int((sum4+sum3+sum2+sum1+sum0)/5)
    # print(sum_avg)
    sum_set = np.array([sum0, sum1, sum2, sum3, sum4])
    print("sum_set:", sum_set)
    # sum_logic = sum_set>=90
    # print("sum_logic:", sum_logic)
    # if sum_avg>=90:
    #     caption = "red"
    # else:
    #     caption = "no target"
    # if sum_avg>=140:
    #     caption = "green"
    # if sum_avg>=200:
    #     caption = "orange"
    # if sum_avg>=270:
    #     caption = "yellow"
    if all(sum_set>=270):
        caption = "yellow"
        print(caption)
    elif all(sum_set>=200):
        caption = "orange"
        print(caption)
    elif all(sum_set>=140):
        caption = "green"
        print(caption)
    elif all(sum_set>=90):
        caption = "red"
        print(caption)
    else:
        caption = "no target"
        print(caption)


    cv.putText(frame0, caption, (10,50), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)


    #####################
    # Display the video
    #####################
    sleep(0.1)
    cv.imshow("Frame0", frame0)
    # cv.imshow("Frameb", b)
    # cv.imshow("Frameg", g)
    # cv.imshow("Framer", r)


    key = cv.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord("p"):
        print("Blue max:", np.max(b))
        print("Green max:", np.max(g))
        print("Red max:", np.max(r))
        # print("Blue average since last pause:", b_total/counter)
        # print("Green average since last pause:", g_total/counter)
        # print("Red average since last pause:", r_total/counter)
        _ = input("Press the anykey to continue.")
        # b_total = 0
        # g_total = 0
        # r_total = 0
        # counter = 0
