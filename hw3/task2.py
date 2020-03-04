#!/usr/bin/env python3

import cv2
import numpy as np
import imutils
from task1 import disp_check, ret_corners

corners_x = 10
corners_y = 7

list_obj_points = [] # list of point vectors in 3d space
list_image_points_l = [] # list of point vectors in the image plane
list_image_points_r = [] # list of point vectors in the image plane

obj_points = np.zeros((corners_x*corners_y,3), dtype = np.float32) ### Is vec3f float32?
obj_points[:,:2] = np.mgrid[0:corners_x,0:corners_y].T.reshape(-1,2)

for num in range(0,32):
    #Left image
    img_path_l = "StereoL"+str(num)+".bmp"
    corners_l, img_l = ret_corners(img_path_l)
    status=True
    cv2.drawChessboardCorners(img_l, (corners_x,corners_y), corners_l, status)
    cv2.imshow("frame", img_l)

    #Right image
    img_path_r = "StereoR"+str(num)+".bmp"
    corners_r, img_r = ret_corners(img_path_r)
    status=True
    cv2.drawChessboardCorners(img_r, (corners_x,corners_y), corners_r, status)
    cv2.imshow("frame", img_r)

    cv2.waitKey(5)
    list_image_points_l.append(corners_l)
    list_image_points_r.append(corners_r)
    list_obj_points.append(obj_points)

cameraMatrix_l = np.load('cameraMatrixL.npy')
distCoeffs_l = np.load('distCoeffsR.npy')

cameraMatrix_r = np.load('cameraMatrixL.npy')
distCoeffs_r = np.load('distCoeffsR.npy')

gray = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)

criteria_specs = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
(_, cm1, dc1, cm2, dc2, R, T, E, F) = cv2.stereoCalibrate(list_obj_points, list_image_points_l, list_image_points_r, cameraMatrix_l, distCoeffs_l, cameraMatrix_r, distCoeffs_r, gray.shape[::-1], criteria=criteria_specs, flags=cv2.CALIB_FIX_INTRINSIC)
# ret = cv2.stereoCalibrate(list_obj_points, list_image_points_l, list_image_points_r, cameraMatrix_l, distCoeffs_l, cameraMatrix_r, distCoeffs_r, gray.shape[::-1], flags=cv2.CALIB_FIX_INTRINSIC, criteria=criteria_specs)
# print(ret)
print("R:", R)
np.save('R.npy', R)
print("T:", T)
np.save('T.npy', T)
print("E:", E)
np.save('E.npy', E)
print("F:", F)
np.save('F.npy', F)

np.save('cm1.npy', cm1)
np.save('dc1.npy', dc1)
np.save('cm2.npy', cm2)
np.save('dc2.npy', dc2)
