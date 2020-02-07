#!/usr/bin/env python3
import numpy as np
import cv2
from task1 import disp_check, ret_corners

corners_h = 7
corners_w = 10

obj_points = []
image_points = []

for num in range(1,41):
    img_path = "AR"+str(num)+".jpg"
    corners, img = ret_corners(img_path)
    print("corners:", corners)
    status=True
    cv2.drawChessboardCorners(img, (corners_w,corners_h), corners, status)
    cv2.imshow("frame", img)
    cv2.waitKey(10)
    img_points.append(corners)
    # cv2.calibrateCamera()
