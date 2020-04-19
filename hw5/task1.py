#!/usr/bin/env python3

import numpy as np
import cv2

# cap = cv2.VideoCapture("./CorridorOriginal.mp4")
# cap = cv2.VideoCapture("./desktop.mp4")
cap = cv2.VideoCapture("./myVid.mp4")


ret, frame_n = cap.read()

#ProcessTrack
gray_n = cv2.cvtColor(frame_n, cv2.COLOR_BGR2GRAY)
PrevPoints = cv2.goodFeaturesToTrack(gray_n, maxCorners=500, qualityLevel=0.1, minDistance=10)

m = 1
win_x, win_y = np.shape(gray_n)[::-1]

cv2.imshow("right:", frame_n)
cv2.waitKey(8000)


while ret:
    for iteration in range(m):
        ret, frame_m = cap.read()
    gray_m = cv2.cvtColor(frame_m, cv2.COLOR_BGR2GRAY)

    print(len(PrevPoints))
    NextPoints, status, err = cv2.calcOpticalFlowPyrLK(gray_n, gray_m, prevPts=PrevPoints, nextPts=None, maxLevel=4)

    frame_n = frame_m
    gray_n = gray_m

    if PrevPoints is not None: # if there are corners detected
        spot = 0
        for Ppoint, Npoint in zip(PrevPoints, NextPoints):
            Px,Py = Ppoint[0]
            Nx, Ny = Npoint[0]
            cv2.circle(frame_n, (Px, Py), 2, (0, 255, 0), 4)
            cv2.line(frame_n, (Px, Py), (Nx, Ny), (0,0,255),2)
            if (Nx<0 or Nx>win_x) or (Ny<0 or Ny>win_y):
                print("yikes on aisle:", spot)
                NextPoints = np.delete(NextPoints, spot, axis=0)
                spot-=1
            spot+=1

    PrevPoints = NextPoints


    cv2.imshow("right:", frame_n)
    cv2.waitKey(1)
