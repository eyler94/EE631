#!/usr/bin/env python3

import cv2

def disp_check(img = cv2.imread("AR1.jpg")):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    status, corners = cv2.findChessboardCorners(gray, (10,7))
    print("Corners:", corners[0])
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray, corners, (5,5), (-1,-1), criteria)
    # if corners is not None: # if there are corners detected
    #             for point in corners: # why is there a ghost artifact in the first element
    #                 x,y = point[0]
    #                 cv2.circle(img, (x, y), 2, (0, 0, 255), 2)
    cv2.drawChessboardCorners(img, (10,7), corners, status)

    frame = img
    cv2.imshow("frame", frame)
    cv2.waitKey(0)

if __name__ == "__main__":
    disp_check()
