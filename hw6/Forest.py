#!/usr/bin/env python3

import numpy as np
import imutils
import cv2

# method of feature points
orb = cv2.ORB_create()

picture_c = cv2.imread('pic1.jpg')
picture = imutils.resize(picture_c, width=600)
# gray = cv2.cvtColor(picture_c, cv2.COLOR_BGR2GRAY)
# _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
# kernel = np.ones((5,5))
# thresh = cv2.dilate(thresh, kernel, iterations = 20)
# picture = cv2.erode(thresh, kernel, iterations = 20)

pic_kp, pic_des = orb.detectAndCompute(picture, None)

cap = cv2.VideoCapture(2)

while True:
    _, image_c = cap.read()
    image = imutils.resize(image_c, width=600)
    # gray = cv2.cvtColor(image_c, cv2.COLOR_BGR2GRAY)
    # _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # kernel = np.ones((5,5))
    # thresh = cv2.dilate(thresh, kernel, iterations = 20)
    # image = cv2.erode(thresh, kernel, iterations = 20)
    img_kp, img_des = orb.detectAndCompute(image, None)

    # Brute Force Matching
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(pic_des, img_des)
    # sort the distance from lower to higher
    matches = sorted(matches, key=lambda x:x.distance)

    # show how many match in picture and image
    # the smaller distance the better is matched  >> why??
    # print(len(matches))
    # for m in matches:
    #     print(m.distance)

    matching_result = cv2.drawMatches(image_c,img_kp,picture_c,pic_kp,matches[:4],None,flags=2)

    # cv2.imshow('picture', pic_kp)
    # cv2.imshow('image', img_kp)
    cv2.imshow('matching_result',matching_result)
    cv2.waitKey(5000)
cv2.destroyAllWindows()
