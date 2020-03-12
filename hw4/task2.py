#!/usr/bin/env python3

import numpy as np
import cv2
import imutils

# buffer = 60
#
# x_l = 360
# y_l = 100
# x_r = 277
# y_r = 100
kernel = np.ones((5,5), np.uint8)
counter = 0
delay_time = 5

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


cap_l = cv2.VideoCapture("./footage_left.avi")
cap_r = cv2.VideoCapture("./footage_right.avi")

while True:
    _, frame_l = cap_l.read()
    frame_l, cent_l = ret_img_and_ball_centroids(frame_l, 295, 295+130, 20, 170,"l")
    print("left cent:", cent_l)
    cv2.imshow("left:", frame_l)

    _, frame_r = cap_r.read()
    frame_r, cent_r = ret_img_and_ball_centroids(frame_r, 212, 212+130, 20, 170,"r")
    print("right cent:", cent_r)
    cv2.imshow("right:", frame_r)

    if not cent_l[0] == 0:# and not cent_r[0] == 0:
        counter+=1
        print("counter:", counter)
        delay_time = 0
        key = cv2.waitKey(delay_time) & 0xFF
        if key==ord('c'):
            print("counter:", counter)
            cv2.imwrite(f'leftframe_{counter}.png',frame_l)
            cv2.imwrite(f'rightframe_{counter}.png',frame_r)
    else:
        key = cv2.waitKey(delay_time)
        counter = 0
