#!/usr/bin/env python3

import cv2
import numpy as np

from glob import glob

pics = glob('*.jpg')

spot_t = 2#int(input("Which target:"))
spot_r = 2#int(input("Which replacement:"))

ratio = 1
orb = cv2.ORB_create()
Brute_Force_Matcher = cv2.BFMatcher.create(normType=cv2.NORM_HAMMING, crossCheck=True)

target = cv2.imread(pics[spot_t])
target_shape = np.shape(target)[1::-1]
target = cv2.resize(target, (int(target_shape[0]*ratio), int(target_shape[1]*ratio)))
target_keyPoints, target_Descriptors = orb.detectAndCompute(target, None)

replacement = cv2.imread(pics[spot_r])
replacement = cv2.resize(replacement, (int(target_shape[0]*ratio), int(target_shape[1]*ratio)))

def ret_puzzle_piece(frame):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_hue = frame_hsv[:,:,0]
    frame_sat = frame_hsv[:,:,1]
    _, hue_thresh = cv2.threshold(frame_hue, 20, 255, cv2.THRESH_BINARY_INV)
    _, sat_thresh = cv2.threshold(frame_sat, 10,2055, cv2.THRESH_BINARY_INV)
    frame_thresh = hue_thresh | sat_thresh
    kernel_3 = np.ones((3,3))
    kernel_5 = np.ones((5,5))
    frame_thresh = cv2.erode(frame_thresh, kernel_5, iterations=4)
    frame_thresh = cv2.dilate(frame_thresh, kernel_3, iterations=10)
    contours, _ = cv2.findContours(frame_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame_thresh = cv2.cvtColor(frame_thresh, cv2.COLOR_GRAY2BGR)
    for spot, contour in enumerate(contours):
        if cv2.contourArea(contour)>1000:
            frame_thresh = cv2.drawContours(frame_thresh, contours, spot, (0,255,0),cv2.FILLED)
    return frame_thresh

cap = cv2.VideoCapture(3)

first = True

key = 'r'
while key != ord('q'):
    ret, frame = cap.read()
    frame_shape = np.shape(frame)[1::-1]
    frame = cv2.resize(frame, (int(frame_shape[0]*ratio), int(frame_shape[1]*ratio)))

    video_keyPoints, video_Descriptors = orb.detectAndCompute(frame, None)

    matches = Brute_Force_Matcher.match(target_Descriptors, video_Descriptors)
    matches = sorted(matches, key=lambda x:x.distance)

    target_points = []
    video_points = []

    if len(matches)>100:
        matches_used = 75
        for ii in range(matches_used):
            target_points.append(target_keyPoints[matches[ii].queryIdx].pt)
            video_points.append(video_keyPoints[matches[ii].trainIdx].pt)

        target_points = np.asarray(target_points).reshape(-1, 1, 2)
        video_points = np.asarray(video_points).reshape(-1, 1, 2)

        homography, mask = cv2.findHomography(target_points[:matches_used], video_points[:matches_used],method=cv2.RANSAC)

        puzzle_piece = ret_puzzle_piece(frame)
        frame_shape = np.shape(frame)[1::-1]
        # warp_puzzle = cv2.warpPerspective(puzzle_piece, homography, frame_shape)
        warp_replacement = cv2.warpPerspective(replacement, homography, frame_shape)
        add_frame_mask = warp_replacement | puzzle_piece
        # fill_gaps = add_frame_mask | warp_replacement
        # matched = cv2.drawMatches(target, target_keyPoints, frame, video_keyPoints, matches[:4],None)
        # cv2.imshow("matched", matched)
        cv2.imshow('Found it!', add_frame_mask)
        key = cv2.waitKey(5)
    else:
        cv2.imshow('Waiting', frame)
        key = cv2.waitKey(5)
        cv2.destroyAllWindows()
