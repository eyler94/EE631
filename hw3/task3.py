#!/usr/bin/env python3
import numpy as np
import cv2
import imutils

def EpiLines(img_name, cameraMatrix, distCoeffs, img_num, F):
    img = cv2.imread(f"./{img_name}.bmp")
    img = imutils.resize(img, width=600)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    undist = cv2.undistort(gray, cameraMatrix, distCoeffs)#, None, cameraMatrix)
    diff = cv2.absdiff(gray,undist)

    features = cv2.goodFeaturesToTrack(undist, maxCorners=3, qualityLevel=0.1, minDistance=200)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(undist, features, (5,5), (-1,-1), criteria)
    x_lines = [0, 600, 0, 600, 0, 600]
    y_lines = []
    if corners is not None: # if there are corners detected
        for spot, point in enumerate(corners): # why is there a ghost artifact in the first element
            x,y = point[0]
            cv2.circle(img, (x, y), 2, (0, 0, 255), 2)
            cv2.circle(img, (x, y), 20, (0, 0, 255), 2)
            lines = cv2.computeCorrespondEpilines(point, img_num, F)
            a,b,c = lines[0][0]
            y_point = -int(c/b)
            y_lines.append(y_point)
            y_point = -int((c+x_lines[spot*2+1])/b)
            y_lines.append(y_point)

    lines = [x_lines, y_lines]
    cv2.imshow("original", img)
    cv2.imshow("undistorted", undist)
    cv2.imshow("difference", diff)
    cv2.imwrite(f"difference_{img_name}.png",diff)
    cv2.waitKey(0)
    return diff, img, lines

if __name__ == "__main__":
    cameraMatrix_l = np.load('cameraMatrixL.npy')
    distCoeffs_l = np.load('distCoeffsR.npy')
    cameraMatrix_r = np.load('cameraMatrixL.npy')
    distCoeffs_r = np.load('distCoeffsR.npy')
    F = np.load('F.npy')
    diff_l, img_l, lines_l = EpiLines('StereoL0',cameraMatrix_l, distCoeffs_l,1,F)
    diff_r, img_r, lines_r = EpiLines('StereoR0',cameraMatrix_r, distCoeffs_r,2,F)
    print("lines_l:", lines_l)
    print("lines_r:", lines_r)
    for spot in range(3):
        cv2.line(img_l, (lines_r[0][spot*2],lines_r[0][spot*2+1]), (lines_r[1][spot*2],lines_r[1][spot*2+1]), (0,255,0), 2)
        cv2.line(img_r, (lines_l[0][spot*2],lines_l[0][spot*2+1]), (lines_l[1][spot*2],lines_l[1][spot*2+1]), (0,255,0), 2)
    cv2.imshow("left", img_l)
    cv2.imshow("right", img_r)
    cv2.waitKey(0)
