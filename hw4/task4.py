#!/usr/bin/env python3
import numpy as np
import cv2
import imutils


if __name__ == "__main__":
    cameraMatrix_l = np.load('cameraMatrixL.npy')
    distCoeffs_l = np.load('distCoeffsL.npy')
    cameraMatrix_r = np.load('cameraMatrixR.npy')
    distCoeffs_r = np.load('distCoeffsR.npy')
    R = np.load('R.npy')
    T = np.load('T.npy')
    R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(cameraMatrix_l, distCoeffs_l, cameraMatrix_r, distCoeffs_r, (640,480), R, T)
    print("R1:", R2)
    print("R2:", R2)
    print("P1:", P1)
    print("P2:", P2)
    print("Q:", Q)
    Q = np.save('Q.npy', Q)
    R1 = np.save('R1.npy',R1)
    R2 = np.save('R2.npy',R2)
    P1 = np.save('P1.npy',P1)
    P2 = np.save('P2.npy',P2)



    # mp1_l, mp2_l = cv2.initUndistortRectifyMap(cameraMatrix_l, distCoeffs_l, R1, P1, (640,480), cv2.CV_32FC2)
    mp1_l, mp2_l = cv2.initUndistortRectifyMap(cameraMatrix_l, distCoeffs_l, R1, P1, (640,480), cv2.CV_32FC2)
    img_l = cv2.imread('stereo_L1.png')
    cv2.imshow("orig left", img_l)
    new_l = cv2.remap(img_l, mp1_l, mp2_l,cv2.INTER_NEAREST)
    for ii in range(1,7):
        cv2.line(new_l,(0,int(480*ii/7)),(640,int(480*ii/7)),(0,255,0),2)
    cv2.imshow("new left", new_l)


    # mp1_r, mp2_r = cv2.initUndistortRectifyMap(cameraMatrix_l, distCoeffs_l, R1, P1, (640,480), cv2.CV_32FC2)
    mp1_r, mp2_r = cv2.initUndistortRectifyMap(cameraMatrix_r, distCoeffs_r, R2, P2, (640,480), cv2.CV_32FC2)
    img_r = cv2.imread('stereo_R1.png')
    cv2.imshow("orig right", img_r)
    new_r = cv2.remap(img_r, mp1_r, mp2_r,cv2.INTER_NEAREST)
    for ii in range(1,7):
        cv2.line(new_r,(0,int(480*ii/7)),(640,int(480*ii/7)),(0,255,0),2)
    cv2.imshow("new right", new_r)


    diff_l = cv2.absdiff(img_l,new_l)
    diff_r = cv2.absdiff(img_r,new_r)
    cv2.imshow("diff left", diff_l)
    cv2.imshow("diff right", diff_r)
    cv2.waitKey(0)
