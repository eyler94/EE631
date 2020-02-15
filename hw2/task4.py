#!/usr/bin/env python3

import numpy as np
import cv2
import pandas as pd

cameraMatrix = np.load('cameraMatrix.npy')
distCoeffs = np.load('distCoeffs.npy')
imagePoints = np.array(pd.read_csv('imagePoints.csv', delimiter=','),dtype=np.float32)
objectPoints = np.array(pd.read_csv('objectPoints3d.csv', delimiter=','),dtype=np.float32)
img = cv2.imread('ObjectWithCorners.jpg')

_, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs)

print("R:\n", cv2.Rodrigues(rvec)[0])
print("T:\n", tvec)
