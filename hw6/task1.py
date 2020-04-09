#!/usr/bin/env python3

import cv2
import imutils

hp_img = cv2.imread("beet.jpg")
hp_img = imutils.resize(hp_img, width=600)

gray = cv2.cvtColor(hp_img, cv2.COLOR_BGR2GRAY)
features = cv2.goodFeaturesToTrack(gray, maxCorners=50, qualityLevel=0.1, minDistance=150)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(gray, features, (5,5), (-1,-1), criteria)
if corners is not None: # if there are corners detected
    for point in corners: # why is there a ghost artifact in the first element
        x,y = point[0]
        cv2.circle(hp_img, (x, y), 2, (0, 0, 255), 2)
        cv2.circle(hp_img, (x, y), 4, (0, 255, 0), 2)

cv2.imshow("Beet", hp_img)
cv2.waitKey(0)
