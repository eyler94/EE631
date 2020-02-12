#!/usr/bin/env python3

import cv2

def disp_check(img = cv2.imread("AR1.jpg"), save_image=False):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    status, corners = cv2.findChessboardCorners(gray, (10,7))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray, corners, (5,5), (-1,-1), criteria)
    cv2.drawChessboardCorners(img, (10,7), corners, status)

    frame = img
    print("frame shape:", frame.shape[::-1])
    cv2.imshow("frame", frame)
    cv2.waitKey(0)
    if save_image:
        cv2.imwrite("AR1_rainbow.png",frame)

def ret_corners(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    status, corners = cv2.findChessboardCorners(gray, (10,7))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray, corners, (5,5), (-1,-1), criteria)
    return corners, img

if __name__ == "__main__":
    disp_check(img = cv2.imread("AR1.jpg"), save_image=True)
