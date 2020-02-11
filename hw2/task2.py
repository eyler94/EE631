#!/usr/bin/env python3
import numpy as np
import cv2
from task1 import disp_check, ret_corners

corners_x = 10
corners_y = 7

list_obj_points = [] # list of point vectors in 3d space
list_image_points = [] # list of point vectors in the image plane

obj_points = np.zeros((corners_x*corners_y,3), dtype = np.float32) ### Is vec3f float32?
obj_points[:,:2] = np.mgrid[0:corners_x,0:corners_y].T.reshape(-1,2)


for num in range(1,41):
    img_path = "AR"+str(num)+".jpg"
    corners, img = ret_corners(img_path)
    status=True
    cv2.drawChessboardCorners(img, (corners_x,corners_y), corners, status)
    cv2.imshow("frame", img)
    cv2.waitKey(5)
    list_image_points.append(corners)
    list_obj_points.append(obj_points)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(list_obj_points, list_image_points, gray.shape[::-1], None, None)
print("Intrinsic parameters:\n", cameraMatrix)
distCoeffs = distCoeffs.T
print("Distortion coeffecients:\n", distCoeffs)#, rvecs, tvecs)

unit_conv = 7.4e-3 ## mm/pix
fsx = cameraMatrix[0,0]
focal_length = fsx*unit_conv
print("Focal length:\n", focal_length)

np.save('cameraMatrix.npy', cameraMatrix)
np.save('distCoeffs.npy', distCoeffs)

from task3 import ShowDistort

ShowDistort('Far',cameraMatrix, distCoeffs)
ShowDistort('Close',cameraMatrix, distCoeffs)
ShowDistort('Turned',cameraMatrix, distCoeffs)
