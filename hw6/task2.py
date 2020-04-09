#!/usr/bin/env python3

import cv2
import numpy as np

ratio = 0.5

target = cv2.imread('beet_crop.jpg')
# target = cv2.rotate(target, cv2.ROTATE_90_CLOCKWISE)
target_shape = np.shape(target)[1::-1]
target = cv2.resize(target, (int(target_shape[0]*ratio), int(target_shape[1]*ratio)))

replacement = cv2.imread('cuc_crop.jpg')
# replacement = cv2.rotate(replacement, cv2.ROTATE_90_CLOCKWISE)
replacement = cv2.resize(replacement, (int(target_shape[0]*ratio), int(target_shape[1]*ratio)))

orb = cv2.ORB_create()

Brute_Force_Matcher = cv2.BFMatcher.create(normType=cv2.NORM_HAMMING, crossCheck=True)

target_keyPoints, target_Descriptors = orb.detectAndCompute(target, None)

cap = cv2.VideoCapture('beet_vid.mp4')

first = True

while True:
    ret, frame = cap.read()
    frame_shape = np.shape(frame)[1::-1]
    # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame = cv2.resize(frame, (int(frame_shape[0]*ratio), int(frame_shape[1]*ratio)))

    video_keyPoints, video_Descriptors = orb.detectAndCompute(frame, None)

    matches = Brute_Force_Matcher.match(target_Descriptors, video_Descriptors)
    matches = sorted(matches, key=lambda x:x.distance)

    target_points = []
    video_points = []

    for ii in range(15):
        target_points.append(target_keyPoints[matches[ii].queryIdx].pt)
        video_points.append(video_keyPoints[matches[ii].trainIdx].pt)

    target_points = np.asarray(target_points).reshape(-1, 1, 2)
    video_points = np.asarray(video_points).reshape(-1, 1, 2)

    homography, mask = cv2.findHomography(target_points, video_points,method=cv2.RANSAC)

    frame_shape = np.shape(frame)[1::-1]
    warp_replacement = cv2.warpPerspective(replacement, homography, frame_shape)

    warp_gray = cv2.cvtColor(warp_replacement, cv2.COLOR_BGR2GRAY)
    _, warp_thresh = cv2.threshold(warp_gray, 1, 255, cv2.THRESH_BINARY_INV)
    warp_mask = cv2.cvtColor(warp_thresh, cv2.COLOR_GRAY2BGR)
    add_frame_mask = frame & warp_mask
    fill_gaps = add_frame_mask | warp_replacement

    cv2.imshow('add frame', fill_gaps)
    cv2.waitKey(1)
