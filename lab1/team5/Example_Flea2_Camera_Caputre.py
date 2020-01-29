import cv2
import numpy as np

# get camera functions
from Flea2Camera import FleaCam

# Setup Camera
cam = FleaCam()

while True:
    # Get Opencv Frame
    frame = cam.getFrame()

    # print(cv_image.shape)
    cv2.imshow('frame',frame)


    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break