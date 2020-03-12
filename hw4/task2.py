#!/usr/bin/env python3

import numpy as np
import cv2


# buffer = 60
#
# x_l = 360
# y_l = 100
# x_r = 277
# y_r = 100
kernel = np.ones((5,5), np.uint8)
counter = 0

def ret_img_and_ball_centroids(img, xl, xh, yl, yh):
    # cv2.rectangle(img,(xl,yl),(xh,yh),(0,255,0),2)
    left_cropped = img[yl:yh, xl:xh]
    left_gray = cv2.cvtColor(left_cropped, cv2.COLOR_BGR2GRAY)
    _, left_thresh = cv2.threshold(left_gray, 50, 255, cv2.THRESH_BINARY)
    left_erode = cv2.erode(left_thresh, kernel, iterations = 2)
    left_dilate = cv2.dilate(left_erode, kernel, iterations = 2)

    contours, _  = cv2.findContours(left_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cent = np.array([0,0])
    if len(contours) > 0:
        max_contour = max(contours,key=cv2.contourArea)
        Image_moment = cv2.moments(max_contour)
        x_center_m = int(Image_moment['m10']/Image_moment['m00'])
        y_center_m = int(Image_moment['m01']/Image_moment['m00'])
        cv2.circle(img, (int(x_center_m+xl),int(y_center_m+yl)), 10, (0,255,0),2)
        cent = np.array([int(x_center_m+xl),int(y_center_m+yl)])
    return img, cent


cap_l = cv2.VideoCapture("./footage_left.avi")
cap_r = cv2.VideoCapture("./footage_right.avi")
_, frame_l = cap_l.read()
_, frame_r = cap_r.read()

while frame_l is not None:
    _, frame_l = cap_l.read()
    frame_l, cent_l = ret_img_and_ball_centroids(frame_l, 295, 295+130, 20, 220)
    print("left cent:", cent_l)
    cv2.imshow("left:", frame_l)

    _, frame_r = cap_r.read()
    frame_r, cent_r = ret_img_and_ball_centroids(frame_r, 212, 342, 20, 220)
    print("right cent:", cent_r)
    cv2.imshow("right:", frame_r)

    if not cent_l[0] == 0 and not cent_r[0] == 0:
        counter+=1
        print("counter:", counter)
        key = cv2.waitKey(0) & 0xFF
        if key==ord('c'):
            print("counter:", counter)
            cv2.imwrite(f'leftframe_{counter}.png',frame_l)
            cv2.imwrite(f'rightframe_{counter}.png',frame_r)
    else:
        key = cv2.waitKey(1)
        counter = 0
