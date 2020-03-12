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

    img_path = "stereo_L1.png"
    corners_l, img_l = ret_corners(img_path)
    cameraMatrix_l = np.load('cameraMatrixL.npy')
    distCoeffs_l = np.load('distCoeffsL.npy')
    R1 = np.load('R1.npy')
    P1 = np.load('P1.npy')
    status=True
    special_corners = [0, 9, -10, -1]
    # print("corners:\n", corners_l[special_corners])
    corners_undistorted_l = cv2.undistortPoints(corners_l[special_corners], cameraMatrix_l, distCoeffs_l, R=R1, P=P1)
    # print("corners_undistorted_l:\n", corners_undistorted_l)
    cv2.drawChessboardCorners(img_l, (2,2), corners_l[special_corners], status)
    cv2.imshow("frame_l", img_l)

    img_path = "stereo_R1.png"
    corners_r, img_r = ret_corners(img_path)
    cameraMatrix_r = np.load('cameraMatrixR.npy')
    distCoeffs_r = np.load('distCoeffsR.npy')
    R2 = np.load('R2.npy')
    P2 = np.load('P2.npy')
    # print("corners:\n", corners_r[special_corners])
    corners_undistorted_r = cv2.undistortPoints(corners_r[special_corners], cameraMatrix_r, distCoeffs_r, R=R2, P=P2)
    # print("corners_undistorted_r:\n", corners_undistorted_r)
    cv2.drawChessboardCorners(img_r, (2,2), corners_r[special_corners], status)
    cv2.imshow("frame_r", img_r)

    points = np.zeros((4,1,3))
    row = 0
    x = 0
    y = 1
    disparity = 2
    for page_iter, page in enumerate(points):
        page[row][x] = corners_undistorted_l[page_iter][row][x]
        page[row][y] = corners_undistorted_l[page_iter][row][y]
        page[row][disparity] = corners_undistorted_l[page_iter][row][x]-corners_undistorted_r[page_iter][row][x]
    # points = points.T
    # print("points:\n", points)
    Q = np.load('Q.npy')
    points_3d = cv2.perspectiveTransform(points,Q)
    print("3d points:", points_3d)

    points = np.zeros((4,1,3))
    row = 0
    x = 0
    y = 1
    disparity = 2
    for page_iter, page in enumerate(points):
        page[row][x] = corners_undistorted_r[page_iter][row][x]
        page[row][y] = corners_undistorted_r[page_iter][row][y]
        page[row][disparity] = corners_undistorted_l[page_iter][row][x]-corners_undistorted_r[page_iter][row][x]
    # points = points.T
    # print("points:\n", points)
    Q = np.load('Q.npy')
    points_3d = cv2.perspectiveTransform(points,Q)
    print("3d points:", points_3d)


    cv2.waitKey(0)
