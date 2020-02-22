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
	cap = cv2.VideoCapture("/dev/video2", cv2.CAP_V4L) 	# ls -ltr /dev/video*
else:
	print("Opening the following video: ", args.get("video"))
	cap = cv2.VideoCapture(args["video"])

def vid_process():
	_, frame = cap.read() 	# Read image
	frame = imutils.resize(frame, height=400) 	# Resize image
	frame = frame[150:, :]
	hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 	# Convert bgr to hsv
	sat = cv2.extractChannel(hsv_image, 1) 	# Extract saturation channel
	_, thresh = cv2.threshold(sat, 50, 255, cv2.THRESH_BINARY)	# Binaryize image
	kernel = np.ones((3,3), np.uint8)
	erode = cv2.erode(thresh, kernel, iterations=17) 	# Remove noise
	dilate = cv2.dilate(erode, kernel, iterations=20) 	# Fill in gaps
	return dilate 	# Return the image
	
def find_angle(frame, num_rows, num_cols):
	# Steering constants
	threshold = 0
	max_degree = 25
	steering_ratio = max_degree/int(num_cols/2)
	h = int(frame.shape[0])
	w = int(frame.shape[1])
	# Determine the grid square that has the minimum number of non-zero pixels and aim for it.
	num_pix_list = [] 	# Initialize an empty list to contain the number of non-zero pixels in each grid
	for row in range(num_rows): 	# Iterate through each row
		for col in range(num_cols): 	# Iterate through each column
			sub_image = frame[int(h*row/num_rows):int(h*(row+1)/num_rows), int(w*col/num_cols):int(w*(col+1)/num_cols)] # select that row and column's grid square
			num_pix = cv2.countNonZero(sub_image)	# Determine the number of non-zero pixels inside the sub-image
			if col == int(num_cols/2) and num_cols%2 != 0:	# Bias the car to stay straight given a certain threshold
				num_pix -= threshold
			num_pix_list.append(num_pix)	# Add the number of non-zero pixels to the list
	min_pix_spot = np.argmin(num_pix_list)	# Find the minimum
	
	# Set the angle based off of the location of the minimum
	min_pix_spot -= int(num_cols/2) # Level the result with the 0-axis
	if num_cols%2 == 0:	# If there are an even number of columns and it's in the second half, we need to add 1 back in to make an even gradiant.
		if min_pix_spot > num_cols/2:
			min_pix_spot+=1
	angle = steering_ratio*min_pix_spot
	return angle


sleep(1)
car = Car_driver() 	# Instantiate the car object
car.drive(.8) 	# Send a speed command to the car

while True:
	dilate = vid_process() 	# Capture and process frame from the video
	angle = find_angle(dilate, 1, 5) 	# Determine the steering angle based off the image and number of rows and columns.
	car.steer(angle) 	# Send the steering command to the car

	# GUI interface stuff. Make sure to comment this out to save processing time.
#	print("Turn:", angle)
#	caption = "Turn " + str(angle) + "!"
#	cv2.putText(dilate, caption, (int(dilate.shape[0]/2),int(dilate.shape[1]/4)), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2)
#	cv2.imshow("frame", dilate)
#	cv2.waitKey(15)
