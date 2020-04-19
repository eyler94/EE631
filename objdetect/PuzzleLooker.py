import numpy as np
import cv2

cap = cv2.VideoCapture(3)

def ret_puzzle_piece(frame):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_hue = frame_hsv[:,:,0]
    frame_sat = frame_hsv[:,:,1]
    _, hue_thresh = cv2.threshold(frame_hue, 20, 255, cv2.THRESH_BINARY_INV)
    _, sat_thresh = cv2.threshold(frame_sat, 10,2055, cv2.THRESH_BINARY_INV)
    frame_thresh = hue_thresh | sat_thresh
    kernel_3 = np.ones((3,3))
    kernel_5 = np.ones((5,5))
    frame_thresh = cv2.erode(frame_thresh, kernel_5, iterations=4)
    frame_thresh = cv2.dilate(frame_thresh, kernel_3, iterations=10)
    contours, _ = cv2.findContours(frame_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for spot, contour in enumerate(contours):
        if cv2.contourArea(contour)>1000:
            frame_thresh = cv2.drawContours(frame, contours, spot, (0,255,0),2)
    return frame_thresh


iter = 0
key='r'
while key!=ord("q"):
    _, frame = cap.read()
    frame_thresh = ret_puzzle_piece(frame)
    cv2.imshow("frame", frame_thresh)
    key = cv2.waitKey(50) & 0xFF

    if key ==ord("c"):
        iter+=1
        print("got here")
        cv2.imwrite(f"./pic{iter}.jpg", frame)
