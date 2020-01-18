#!/usr/bin/env python3
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils

# vs = VideoStream(0).start()
vs = cv2.VideoCapture(0)
vs.set(cv2.CAP_PROP_FPS, 15)
# vs.set(cv.CAP_PROP_FPS, 15)
setting = "o" # ordinary
print("Options:\no: Ordinary\nt: Thresholding\na: Canny Difference\nd: Differencing\nl: Line Detection\nc: Corner Detection\nq: quit")

while True:
    if setting=="o": # Ordinary
        ret, frame = vs.read()
        frame = imutils.resize(frame, width=600)
        cv2.imshow("Eyler", frame)
        key = cv2.waitKey(1) & 0xFF
    elif setting=="t": # Thresholding
        ret, frame = vs.read()
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        cv2.imshow("Thresholding", thresh)
        key = cv2.waitKey(1) & 0xFF
    elif setting=="a": # Canny difference
        ret, frame = vs.read()
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 30, 150)
        cv2.imshow("Canny (edge detection)", edge)
        key = cv2.waitKey(1) & 0xFF
    elif setting=="d": # Differencing
        ret, frame0 = vs.read()
        frame0 = imutils.resize(frame0, width=600)
        gray0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
        ret, frame1 = vs.read()
        frame1 = imutils.resize(frame1, width=600)
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray0,gray1)
        # diff = gray0-gray1
        cv2.imshow("Differencing", diff)
        key = cv2.waitKey(1) & 0xFF
    elif setting=="l": # line detection
        ret, frame = vs.read()
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 30, 150)
        lines = cv2.HoughLines(edge, 1, np.pi/180, 200)
        if lines is not None:
            for line in lines:
                for radius, theta in line:
                    c_theta = np.cos(theta)
                    s_theta = np.sin(theta)
                    x0 = c_theta*radius
                    y0 = s_theta*radius
                    x1 = int(x0 - 1000*s_theta)
                    y1 = int(y0 + 1000*c_theta)
                    x2 = int(x0 + 1000*s_theta)
                    y2 = int(y0 - 1000*c_theta)
                    cv2.line(frame, (x1,y1), (x2,y2), (0,0,255), 2)
        cv2.imshow("Line detection", frame)
        key = cv2.waitKey(1) & 0xFF
    elif setting=="c": # Corner detection
        ret, frame = vs.read()
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_f32 = np.float32(gray)
        corner = cv2.cornerHarris(gray, 2, 3, 0.04)
        corner_dil = cv2.dilate(corner,None)
        _, corner_thresh = cv2.threshold(corner_dil, 0.01*corner_dil.max(), 255, cv2.THRESH_BINARY)
        corner_ui8 = np.uint8(corner_thresh)

        #### Andy's code
        _, _, _, centroids = cv2.connectedComponentsWithStats(corner_ui8) # don't know :|

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001) # create object of 'criteria' data
        corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria) # find sub pixel corners

        if corners is not None: # if there are corners detected
            for point in corners[1:]: # why is there a ghost artifact in the first element
        ####
                cv2.circle(frame, (point[0], point[1]), 2, (0, 0, 255), 2)

        cv2.imshow("Corner Detection", frame)
        key = cv2.waitKey(1) & 0xFF

    if key == ord("q"): # quit
        vs.release()
        cv2.destroyAllWindows()
        break
    elif key== ord("o"): # ordinary
        cv2.destroyAllWindows()
        setting="o"
    elif key == ord("t"): # thresholding
        cv2.destroyAllWindows()
        setting="t"
    elif key == ord("a"): # Canny
        cv2.destroyAllWindows()
        setting="a"
    elif key == ord("c"): # Corner
        cv2.destroyAllWindows()
        setting="c"
    elif key == ord("d"): # Differencing
        cv2.destroyAllWindows()
        setting="d"
    elif key == ord("l"): # Line detection
        cv2.destroyAllWindows()
        setting="l"
