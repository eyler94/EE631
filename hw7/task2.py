#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.pyplot as plt

ratio = 1

def return_cropped_image(img_path):
    image = cv2.imread(img_path)
    image_shape = np.shape(image)[1::-1]
    image_width = image_shape[0]
    image_height = image_shape[1]
    image_crop = image[int(image_height/4):int(image_height*5/7), :image_width]
    gray = cv2.cvtColor(image_crop, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour)>10000:
            x, y, width, height = cv2.boundingRect(contour)
            y+=int(image_height/4)
    # image = image[y:y+height, x:x+width]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, x, y, width, height

spot = 1
gray_n, x, y, width, height = return_cropped_image(f'T{spot}.jpg')
win_x, win_y = np.shape(gray_n)[1::-1]

PrevPoints = cv2.goodFeaturesToTrack(gray_n[y:y+height, x:x+width], maxCorners=500, qualityLevel=0.01, minDistance=6).reshape((-1,2))
PrevPoints[:,0]+=x
PrevPoints[:,1]+=y

dis_list = []

frame_list = list(range(2,19))

for spot in range(2,19):
    gray_m, _, _, _, _ = return_cropped_image(f'T{spot}.jpg')

    NextPoints, status, err = cv2.calcOpticalFlowPyrLK(gray_n, gray_m, prevPts=PrevPoints, nextPts=None, maxLevel=2)
    gray_n = gray_m
    frame_n = cv2.cvtColor(gray_n, cv2.COLOR_GRAY2BGR)

    if PrevPoints is not None: # if there are corners detected
        spot = 0
        a_list = []
        for Ppoint, Npoint in zip(PrevPoints, NextPoints):
            Px,Py = Ppoint
            Nx, Ny = Npoint
            xp = np.abs(Nx-win_x/2)
            x = np.abs(Px-win_x/2)
            if x != 0:
                a_list.append(xp/x)
            cv2.circle(frame_n, (Px, Py), 2, (0, 255, 0), 4)
            cv2.line(frame_n, (Px, Py), (Nx, Ny), (0,0,255),2)
            if (Nx<0 or Nx>win_x) or (Ny<0 or Ny>win_y):
                print("yikes on aisle:", spot)
                NextPoints = np.delete(NextPoints, spot, axis=0)
                spot-=1
            spot+=1
        a = np.mean(a_list)
        dis_list.append(a/(a-1)*15.25)


    PrevPoints = NextPoints


    cv2.imshow("right:", frame_n)
    cv2.waitKey(5)

coef = np.polyfit(frame_list, dis_list, 1)
poly = np.poly1d(coef)
framez = np.linspace(0,50,100)
dis = poly(framez)
dis_expect = poly(0)

fig = plt.figure()
plt.plot(framez, dis)
plt.plot(frame_list, dis_list,'bh')
plt.title(f'Distance to impact: {dis_expect} mm')
plt.xlabel('Frames')
plt.ylabel('Distance to impact (mm)')
plt.xlim([-1,50])
plt.ylim(bottom=0)
plt.show()
