#!/usr/bin/env python3

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

imgL = cv.imread('stereo_L9.png')
imgL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
imgR = cv.imread('stereo_R9.png')
imgR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)
cv.imshow("pic", imgL)
cv.waitKey(0)
disp = 16*4
blck = 51
stereo = cv.StereoBM_create(numDisparities=disp, blockSize=blck)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
plt.show()
