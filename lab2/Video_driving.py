#!/usr/bin/env python3

import numpy as np
import cv2
import imutils
from CarDriver import Car_driver

import argparse
from time import sleep

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to video file.")
args = vars(ap.parse_args())

if not args.get("video"):
	print("Using camcam.")
	# initialize the video stream, pointer to output video file, and frame dimensions
	cap = cv2.VideoCapture("/dev/video2", cv2.CAP_V4L)			# ls -ltr /dev/video*
else:
	print("Opening the following video: ", args.get("video"))
	cap = cv2.VideoCapture(args["video"])

def Vid_process():
	_, frame = cap.read()										# Read image
	frame = imutils.resize(frame, height=400)					# Resize image
	frame = frame[150:, :]
	hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)			# Convert bgr to hsv
	sat = cv2.extractChannel(hsv_image, 1)						# Extract saturation channel
	_, thresh = cv2.threshold(sat, 50, 255, cv2.THRESH_BINARY)	# Binaryize image
	kernel = np.ones((3,3), np.uint8)
	erode = cv2.erode(thresh, kernel, iterations=17)			# Remove noise
	dilate = cv2.dilate(erode, kernel, iterations=20)			# Fill in gaps
	return dilate
	
def Pix_counter(frame):
	frame_l = frame[:,:int(frame.shape[1]/2)]					# Left half of image
	num_pix_l = cv2.countNonZero(frame_l)						# Number of nonzero pixels in left image
	frame_r = frame[:,int(frame.shape[1]/2):]					# Right half of image
	num_pix_r = cv2.countNonZero(frame_r)						# Number of nonzero pixels in right image
	return num_pix_l, num_pix_r

sleep(1)
car = Car_driver()
car.drive(.8)
threshold = 9000
max_val = 50651
max_degree = 30
steering = max_degree/max_val
while True:
	dilate = Vid_process()
	num_pix_l, num_pix_r = Pix_counter(dilate)
	diff = num_pix_r - num_pix_l
	if abs(diff) > max_val:
		max_val = abs(diff)
		print("max:", max_val)
	if abs(diff) > threshold:
		caption = "Turn " + str(diff) + "!"
		angle = -diff*steering
		print("diff:", angle)
		car.steer(angle)
	else: 
		caption = "Go straight!"
		car.steer(0)
#		print("go straight")
#	cv2.putText(dilate, caption, (int(dilate.shape[0]/2),int(dilate.shape[1]/4)), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2)
	# Display image
	cv2.imshow("frame", dilate)
	cv2.waitKey(15)
