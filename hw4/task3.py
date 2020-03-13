#!/usr/bin/env python3

import numpy as np
import cv2


buffer = 60

x_l = 360
y_l = 100
x_r = 277
y_r = 100
kernel = np.ones((5,5))
counter = 0
found_ball = False

def ret_img_and_ball_centroids(img, xl, xh, yl, yh,side):
    image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.copy()
    cv2.rectangle(img,(xl,yl),(xh,yh),(0,255,0),2)
    image_cropped = image_gray[yl:yh, xl:xh]
    _, image_thresh = cv2.threshold(image_cropped, 60, 255, cv2.THRESH_BINARY)
    image_erode = cv2.erode(image_thresh, kernel, iterations = 1)
    image_dilate = cv2.dilate(image_erode, kernel, 2)
    cv2.imshow(f"dilate{side}", image_dilate)
    contours, _  = cv2.findContours(image_dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours = imutils.grab_contours(contours)
    cent = np.array([0,0])
    if len(contours) > 0:
        print("contours:", contours)
        max_contour = max(contours,key=cv2.contourArea)
        Image_moment = cv2.moments(max_contour)
        x_center_m = int(Image_moment['m10']/Image_moment['m00'])
        y_center_m = int(Image_moment['m01']/Image_moment['m00'])
        cv2.circle(img, (int(x_center_m+xl),int(y_center_m+yl)), 10, (0,255,0),2)
        cent = np.array([int(x_center_m+xl),int(y_center_m+yl)])
    return img, cent

Q = np.load('Q.npy')

cameraMatrix_l = np.load('cameraMatrixL.npy')
distCoeffs_l = np.load('distCoeffsL.npy')
R1 = np.load('R1.npy')
P1 = np.load('P1.npy')
cap_l = cv2.VideoCapture("./footage_left.avi")
_, frame_l = cap_l.read()

cameraMatrix_r = np.load('cameraMatrixR.npy')
distCoeffs_r = np.load('distCoeffsR.npy')
R2 = np.load('R2.npy')
P2 = np.load('P2.npy')
cap_r = cv2.VideoCapture("./footage_right.avi")
_, frame_r = cap_r.read()


while frame_l is not None:
    _, frame_l = cap_l.read()
    frame_l, cent_l = ret_img_and_ball_centroids(frame_l, 295, 295+130, 20, 170,"l")
    print("left cent:", cent_l)
    cv2.imshow("left:", frame_l)

    _, frame_r = cap_r.read()
    frame_r, cent_r = ret_img_and_ball_centroids(frame_r, 212, 212+130, 20, 170,"r")
    print("right cent:", cent_r)
    cv2.imshow("right:", frame_r)

    if cent_l[0] == 0 or cent_r[0] == 0:
        key = cv2.waitKey(1)
        if counter>20:
            print("3d points:", points_3d)
            np.save('points_3d.npy',points_3d)
            break
    else:
        counter+=1
        cent_l = np.array([[[cent_l]]],dtype=np.float32)
        cent_r = np.array([[[cent_r]]],dtype=np.float32)
        print("cent_l:", cent_l[0])
        corners_undistorted_l = cv2.undistortPoints(cent_l[0], cameraMatrix_l, distCoeffs_l, R=R1, P=P1)
        corners_undistorted_r = cv2.undistortPoints(cent_r[0], cameraMatrix_r, distCoeffs_r, R=R2, P=P2)
        points = np.zeros((1,1,3))
        row = 0
        x = 0
        y = 1
        disparity = 2
        for page_iter, page in enumerate(points):
            page[row][x] = cent_l[0][page_iter][row][x]
            page[row][y] = cent_l[0][page_iter][row][y]
            page[row][disparity] = cent_l[0][page_iter][row][x]-cent_r[0][page_iter][row][x]
        if not found_ball:
            print("points:", points)
            points_3d = cv2.perspectiveTransform(points,Q)
        else:
            print("points:", points)
            points_3d = np.vstack((points_3d,cv2.perspectiveTransform(points,Q)))
        found_ball = True

points_catcher = points_3d-np.array([11.5, 29.5, 21.5])

import matplotlib.pyplot as plt
fig1 = plt.figure(1)
plt.plot(points_catcher.T[2],points_catcher.T[0])
