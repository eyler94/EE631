#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.pyplot as plt

cameraMatrix = np.array([[825.0900600547, 0, 331.6538103208],
                        [0, 824.2672147458, 252.9284287373],
                        [0, 0, 1]])
fsx = cameraMatrix[0,0]
unit_conv = 7.4e-3 ## mm/pix
focal_length = fsx*unit_conv
can_width = 59 #mm

dist_list = []
frame_list = list(range(19))
dist_prev = 0

for spot in range(1,19):
    frame = cv2.imread(f'T{spot}.jpg')
    frame_shape = np.shape(frame)[1::-1]
    frame_width = frame_shape[0]
    frame_height = frame_shape[1]
    frame_crop = frame[int(frame_height/4):int(frame_height*5/7), :frame_width]
    gray = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)
    # kernel = np.ones((5,5))
    # dilate = cv2.dilate(thresh, kernel, iterations = 3)
    # mask = cv2.erode(dilate, kernel, iterations = 4)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    frame_mask = frame_crop & mask
    for contour in contours:
        if cv2.contourArea(contour)>10000:
            x, y, width, height = cv2.boundingRect(contour)
            y+=int(frame_height/4)
            dist = can_width*focal_length/width
            dist_diff = dist_prev - dist
            dist_prev = dist
            print("dist_ diff:", dist_diff)
            dist_list.append(dist)
            # caption = f'The can is {dist} mm away.'
            # print(caption)
    cv2.rectangle(frame, (x, y), (x+width, y+height), (255,255,0),2)
    cv2.imshow("frame", frame)
    cv2.waitKey(0)
