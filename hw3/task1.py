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

    for image in image_set:

        list_obj_points = [] # list of point vectors in 3d space
        list_image_points = [] # list of point vectors in the image plane

        obj_points = np.zeros((corners_x*corners_y,3), dtype = np.float32)
        obj_points[:,:2] = np.mgrid[0:corners_x,0:corners_y].T.reshape(-1,2)


        for num in range(0,32):
            img_path = image+str(num)+".png"
            corners, img = ret_corners(img_path)
            status=True
            cv2.drawChessboardCorners(img, (corners_x,corners_y), corners, status)
            cv2.imshow("frame", img)
            cv2.waitKey(5)
            list_image_points.append(corners)
            list_obj_points.append(obj_points)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(list_obj_points, list_image_points, gray.shape[::-1], None, None)
        print(f"Intrinsic parameters for camera  {image}:\n", cameraMatrix)
        distCoeffs = distCoeffs.T
        print(f"Distortion coeffecients for camera {image}:\n", distCoeffs)#, rvecs, tvecs)

        unit_conv = 7.4e-3 ## mm/pix
        fsx = cameraMatrix[0,0]
        focal_length = fsx*unit_conv
        print(f"Focal length for camera {image}:\n", focal_length)

        np.save(f'cameraMatrix{image}.npy', cameraMatrix)
        np.save(f'distCoeffs{image}.npy', distCoeffs)
