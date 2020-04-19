#!/usr/bin/env python3

import cv2
import numpy as np

from glob import glob

pics = glob('*.jpg')

print(pics)
spot_t = int(input("Which target:"))
spot_r = int(input("Which replacement:"))

ratio = 1
orb = cv2.ORB_create()
Brute_Force_Matcher = cv2.BFMatcher.create(normType=cv2.NORM_HAMMING, crossCheck=True)

target = cv2.imread(pics[spot_t])
target_shape = np.shape(target)[1::-1]
target = cv2.resize(target, (int(target_shape[0]*ratio), int(target_shape[1]*ratio)))
target_keyPoints, target_Descriptors = orb.detectAndCompute(target, None)

replacement = cv2.imread(pics[spot_r])
replacement = cv2.resize(replacement, (int(target_shape[0]*ratio), int(target_shape[1]*ratio)))

cap = cv2.VideoCapture(3)

first = True

while True:
    ret, frame = cap.read()
    frame_shape = np.shape(frame)[1::-1]
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
    _, thresh_noninv = cv2.threshold(warp_gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh_noninv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    fill_gaps = cv2.drawContours(frame,contours,0,(0,255,0),2)
    cv2.imshow('add frame', frame)
    _, warp_thresh = cv2.threshold(warp_gray, 1, 255, cv2.THRESH_BINARY_INV)
    warp_mask = cv2.cvtColor(warp_thresh, cv2.COLOR_GRAY2BGR)
    add_frame_mask = frame & warp_mask
    fill_gaps = add_frame_mask | warp_replacement


    matched = cv2.drawMatches(target, target_keyPoints, frame, video_keyPoints, matches[:4],None)
    cv2.imshow("matched", matched)
    # cv2.imshow('spoof', fill_gaps)
    cv2.waitKey(2000)
