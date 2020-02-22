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

# frame grid params
width = 6
height = 4

# generate decision matrix
decision_matrix = np.ones((height, width))
decision_matrix = np.asarray(decision_matrix)
for i in range(height):
	decision_matrix[i, :] = decision_matrix[i, :] * i
for i in range(width):
	if i < width/2:
		decision_matrix[:, i] = decision_matrix[:, i] * i
	else:
		decision_matrix[:, i] = decision_matrix[:, i] * -(width-i-1)
decision_matrix[height-1, 0] = 1
decision_matrix[height-1, width-1] = -1
decision_matrix[0, int(width/2-1)] = 1
decision_matrix[0, int(width/2)] = -1
decision_matrix = decision_matrix * (30 / decision_matrix.max())

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
	threshold = 50
	max_degree = 25
	steering_ratio = max_degree/int(num_cols/2)
	h = int(frame.shape[0])
	w = int(frame.shape[1])
	# Determine the grid square that has the minimum number of non-zero pixels and aim for it.
	num_pix_mat = np.zeros((num_rows, num_cols)) 	# Initialize an empty list to contain the number of non-zero pixels in each grid
	for row in range(num_rows): 	# Iterate through each row
		for col in range(num_cols): 	# Iterate through each column
			sub_image = frame[int(h*row/num_rows):int(h*(row+1)/num_rows), int(w*col/num_cols):int(w*(col+1)/num_cols)] # select that row and column's grid square
			num_pix = cv2.countNonZero(sub_image)	# Determine the number of non-zero pixels inside the sub-image
			num_pix_mat[row, col] = num_pix
	num_pix_mat[num_pix_mat < threshold] = 0
	num_pix_mat[num_pix_mat >= threshold] = 1
	
	options_mat = np.multiply(decision_matrix, num_pix_mat)
	ind = np.argmax(abs(options_mat))
	angle = options_mat.flatten()[ind]
	
	return angle


sleep(1)
car = Car_driver() 	# Instantiate the car object
car.drive(.8) 	# Send a speed command to the car

while True:
	dilate = vid_process() 	# Capture and process frame from the video
	angle = find_angle(dilate, height, width) 	# Determine the steering angle based off the image and number of rows and columns.
	car.steer(angle) 	# Send the steering command to the car

	# GUI interface stuff. Make sure to comment this out to save processing time.
#	print("Turn:", angle)
#	caption = "Turn " + str(angle) + "!"
#	cv2.putText(dilate, caption, (int(dilate.shape[0]/2),int(dilate.shape[1]/4)), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2)
#	cv2.imshow("frame", dilate)
#	cv2.waitKey(15)
