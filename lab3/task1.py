#!/usr/bin/env python3
import numpy as np
import cv2
import imutils

search_kernel = 11
max_iter = 30

def ret_corners(img_path, corners_x=10, corners_y=7):
    img = cv2.imread(img_path)
    # img = imutils.resize(img, width=600)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    status, corners = cv2.findChessboardCorners(gray, (corners_x,corners_y), None)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iter, 0.001)
    corners = cv2.cornerSubPix(gray, corners, (search_kernel,search_kernel), (-1,-1), criteria)
    return corners, img

if __name__=="__main__":

    corners_x = 10
    corners_y = 7

    image_set = ["L", "R"]

    for pic in image_set:
        img_path = "stereo_"+pic+"1.png"
        cameraMatrix = np.load(f'cameraMatrix{pic}.npy')
        distCoeffs = np.load(f'distCoeffs{pic}.npy')
        corners, img = ret_corners(img_path)
        status=True
        special_corners = [0, 9, -10, -1]
        corners_undistorted = cv2.undistortPoints(corners[special_corners], cameraMatrix, distCoeffs)
        print("dst:", corners_undistorted)
        # points_3d = cv2.(corners_undistorted, )
        cv2.drawChessboardCorners(img, (2,2), corners[special_corners], status)
        cv2.imshow("frame", img)
        cv2.waitKey(0)
