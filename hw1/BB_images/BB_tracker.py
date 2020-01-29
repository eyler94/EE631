#!/usr/bin/env python3
import numpy as np
import cv2
import imutils

pic_list = ["06", "07", "08", "09"]

for num in range(10,41):
    pic_list.append(str(num))

header_list = ["1R", "1L"]
step = 1


for header in header_list:
    filename = header + "05" + ".jpg"
    img0 = cv2.imread(filename)

    for pic in pic_list:
        filename = header + pic + ".jpg"
        img1 = cv2.imread(filename)
        diff = cv2.absdiff(img0,img1)
        _, thresh = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)
        mask = cv2.erode(thresh, None, iterations=3)
        mask = cv2.dilate(mask, None, iterations=3)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 1000, 1, 100, 1, 0, 25)
        for circle_iter in circles:
            for prop_iter in circle_iter:
                x, y, r = prop_iter
                cv2.circle(img1, (x, y), r, (0,0,255), 3)
        cv2.imshow("img1", img1)
        cv2.waitKey(10)
