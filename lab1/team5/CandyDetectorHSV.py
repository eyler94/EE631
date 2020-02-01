# ------------------------------------------------------------------------------------------------ IMPORT LIBRARIES ----
import numpy as np
import cv2 as cv
from Flea2Camera import FleaCam
from typing import NamedTuple
from copy import deepcopy


# -------------------------------------------------------------------------------------------------- CUSTOM CLASSES ----
class ConfidenceDisp(NamedTuple):  # custom class to store pertinent information to displaying confidence info
    orig: list  # coordinates (top left corner) of display
    scale: list  # number of pixels in x and y direction per tick
    spacing: int  # horizontal spacing in pixels between bars
    filled: bool  # flag for filling in (or not) rectangle -- true: filled; false: outline
    thickness: int  # thickness of rectangle if not filled


# ------------------------------------------------------------------------------------------------- USER PARAMETERS ----
debugFlag = False  # flag indicating whether or not to printout debug statements to console
beltThreshold = 20  # average of red, green, and blue max values for belt thresholding/detection
erodeIterations = 2  # erode iteration number
dilateIterations = 10  # dilate iteration number
# initialize paramters for confidence display
dispParams = ConfidenceDisp(orig=[8, 50], scale=[5, 15], spacing=8, filled=True, thickness=1)
yellow = (68, 179, 233)  # yellow bgr value
orange = (48, 87, 232)
red = (40, 37, 141)  # red bgr value
green = (65, 112, 83)  # green bgr value
purple = (60, 40, 60)

# hsv_1sig = np.array([[]])
hsv_avg = np.array([[125, 123, 233],
                    [92,65,114],
                    [138,145,226],
                    [147,150,137],
                    [45,35,40]]).T
hsv_rad = np.array([11, 22, 20, 20, 11])*2

print("hsv:\n",hsv_avg)
print("hsv_rad:\n",hsv_rad)

# ----------------------------------------------------------------------------------- VARIABLES AND INITIALIZATIONS ----
cap = FleaCam()  # initialize flea camera to read video
firstFrame = True  # flag indicating first tick of unconditional loop
previousFrame = []  # array to hold previous frame data
confidenceVals = [0, 0, 0, 0, 0]  # confidence values for spree colors
words = ['yellow', 'green', 'orange', 'red', 'purpur']


# ---------------------------------------------------------------------------------------------- UNCONDITIONAL LOOP ----
while True:
    # check if user wants to quit program
    k = cv.waitKey(1) & 0xFF  # read key from keyboard (wait maximum of 1ms)
    if k == 27:  # see if read key is 'esc'
        break  # if so, break from unconditional while loop

    frame = cap.getFrame()  # get frame for this tick of loop
    displayFrame = frame.copy()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # check if is not the first time through the loop - ie, there is previous frame data
    if not firstFrame:
        # process camera data
        diff = cv.absdiff(frame, previousFrame)  # take difference of previous and current frame
        blur = cv.GaussianBlur(diff, (5, 5), 0)  # blur image using gaussian distribution
        erode = cv.erode(blur, None, iterations=erodeIterations)  # erode to remove noise
        dilate = cv.dilate(erode, None, iterations=dilateIterations)  # dilate to enlarge information data
        h, s, v = cv.split(dilate)  # split frame into blue, green, and red data arrays
        h = np.max(np.uint32(h))  # find maximum blue value from frame
        s = np.max(np.uint32(s))  # find maximum green value from frame
        v = np.max(np.uint32(v))  # find maximum red value from frame

        # Find difference between measured and average HSV
        list_norm = []
        hsv_diff = hsv_avg - np.array([[h],[s],[v]])
        for col in range(5):
            list_norm.append(np.linalg.norm(hsv_diff[:,col],2))
        color = np.argmin(list_norm)

        if list_norm[color]<hsv_rad[color]:
            confidenceVals[color] +=1
        else:  # only belt found in frame
            confidenceVals = [0, 0, 0, 0, 0]  # reset confidence values to prepare for next greengoldfish
    else:  # if first time through loop
        firstFrame = False  # unset flag to indicate no longer first time through loop
        confidenceVals = [0, 0, 0, 0, 0]  # reset confidence values to prepare for next goldfish

    previousFrame = frame  # store current frame as previous, preparatory to receiving a new frame next tick

    for i in range(len(confidenceVals)):  # work through possible goldfish colors for confidence display
        # calculate (x, y) for starting point
        p1x = dispParams.orig[0]  # top left x coord
        p1y = dispParams.orig[1] + ((dispParams.scale[1] + dispParams.spacing) * i)  # top left y coord
        # calculate (x, y) for ending point (relative to starting point)
        p2x = p1x + (dispParams.scale[0] * confidenceVals[i])  # bottom right x coord
        p2y = p1y + dispParams.scale[1]  # bottom right y coord

        # words = ['yellow', 'orange', 'red', 'green', 'purpur']

        if i == 0:  # displaying yellow bar
            clr = yellow  # set color to yellow
        elif i == 1:  # displaying orange bar
            clr = green  # set color to orange
        elif i == 2:  # displaying red bar
            clr = orange  # set color to red
        elif i == 3:
            clr = red
        elif i == 4:
            clr = purple
        else:  # uncertain case
            clr = (255, 255, 255)  # white color
        fill = -1 if dispParams.filled else dispParams.thickness  # determine if rectangle will be filled in or not
        displayFrame = cv.rectangle(displayFrame, (p1x, p1y), (p2x, p2y), clr, fill)  # draw rectangle on frame
        if np.average(confidenceVals) == 0:
            caption = ""
        else:
            caption = words[np.argmax(confidenceVals)]
    cv.putText(displayFrame, caption, (15, 30), cv.QT_FONT_NORMAL, .6, (255, 255, 255), 1, cv.LINE_AA)
    cv.imshow('Spree Color Detection', displayFrame)  # display frame

cv.destroyAllWindows()
exit()
