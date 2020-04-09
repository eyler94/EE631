#!/usr/bin/env python3

import cv2
import numpy as np

ratio = 1

orb = cv2.ORB_create()
Brute_Force_Matcher = cv2.BFMatcher.create(normType=cv2.NORM_HAMMING, crossCheck=True)

def return_cropped_image_keypoints_and_descriptors(img_path):
    image = cv2.imread(img_path)
    image_shape = np.shape(image)[1::-1]
    image_width = image_shape[0]
    image_height = image_shape[1]
    image_crop = image[int(image_height/4):int(image_height*5/7), :image_width]
    gray = cv2.cvtColor(image_crop, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    image_mask = image_crop & mask

    image = cv2.resize(image, (int(image_shape[0]*ratio), int(image_shape[1]*ratio)))
    image_keyPoints, image_Descriptors = orb.detectAndCompute(image, None)

    return image_mask, image_keyPoints, image_Descriptors

spot = 1
frame_n, kp_n, des_n = return_cropped_image_keypoints_and_descriptors(f'T{spot}.jpg')

for spot in range(2,19):
    frame_m, kp_m, des_m = return_cropped_image_keypoints_and_descriptors(f'T{spot}.jpg')

    matches = Brute_Force_Matcher.match(des_n, des_m)
    matches = sorted(matches, key=lambda x:x.distance)

    points_n = []
    points_m = []
    x_diff = []

    for ii in range(1):
        points_n.append(kp_n[matches[ii].queryIdx].pt)
        points_m.append(kp_m[matches[ii].trainIdx].pt)
        print("points_m:", kp_m[matches[ii].queryIdx].pt[0]/kp_n[matches[ii].queryIdx].pt[0])

    points_n = np.asarray(points_n).reshape(-1, 1, 2)
    points_m = np.asarray(points_m).reshape(-1, 1, 2)

    matched = cv2.drawMatches(frame_n, kp_n, frame_m, kp_m, matches[:20], None)
    cv2.imshow('matched', matched)
    cv2.waitKey(0)
    frame_n = frame_m.copy()
    kp_n = kp_m.copy()
    des_n = des_m.copy()
