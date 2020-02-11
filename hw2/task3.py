#!/usr/bin/env python3
import numpy as np
import cv2

def ShowDistort(img_name, cameraMatrix, distCoeffs):
    img = cv2.imread(f"./{img_name}.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    undist = cv2.undistort(gray, cameraMatrix, distCoeffs, None, cameraMatrix)
    diff = cv2.absdiff(gray,undist)
    cv2.imshow("original", gray)
    cv2.imshow("undistorted", undist)
    cv2.imshow("difference", diff)
    cv2.imwrite(f"difference_{img_name}.png",diff)
    cv2.waitKey(0)
    return diff

if __name__ == "__main__":
    cameraMatrix = np.load('cameraMatrix.npy')
    distCoeffs = np.load('distCoeffs.npy')
    ShowDistort('Far',cameraMatrix, distCoeffs)
    ShowDistort('Close',cameraMatrix, distCoeffs)
    ShowDistort('Turned',cameraMatrix, distCoeffs)
