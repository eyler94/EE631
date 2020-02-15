#!/usr/bin/env python3

import numpy as np
import cv2
import task3

cameraMatrix = np.load('cameraMatrix_check.npy')
distCoeffs = np.load('distCoeffs_check.npy')

task3.ShowDistort('checkerboard0', cameraMatrix, distCoeffs)
task3.ShowDistort('checkerboard1', cameraMatrix, distCoeffs)
task3.ShowDistort('checkerboard2', cameraMatrix, distCoeffs)
