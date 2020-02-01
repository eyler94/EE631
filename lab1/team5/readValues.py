import numpy as np
import cv2 as cv
from Flea2Camera import FleaCam

beltThreshold = 30

cap = FleaCam()
color_counter = 0

yellow = []
orange = []
red = []
green = []

while True:
    k = cv.waitKey(1) & 0xFF
    if k == ord('y'):
        color_counter = 0
    elif k == ord('o'):
        color_counter = 1
    elif k == ord('r'):
        color_counter = 2
    elif k == ord('g'):
        color_counter = 3
    elif k == 27:
        break
    else:
        pass
    #_, frame0 = cap.read()
    frame0 = cap.getFrame()
    #####################
    # Work the video
    #####################
    #_, frame1 = cap.read()
    frame1 = cap.getFrame()
    if frame1 is None:
        break

    frame0 = cv.cvtColor(frame0, cv.COLOR_BGR2HSV)
    frame1 = cv.cvtColor(frame1, cv.COLOR_BGR2HSV)
    diff = cv.absdiff(frame0,frame1)
    blur = cv.GaussianBlur(diff, (5,5), 0)
    erode = cv.erode(blur, None, iterations=3)
    dilate = cv.dilate(erode, None, iterations=10)

    frame = dilate
    b, g, r = cv.split(frame)
    b = np.max(np.uint32(b))
    g = np.max(np.uint32(g))
    r = np.max(np.uint32(r))
    check = np.array([b, g, r])>=20
    if all(check):
        # print("Blue max:", np.max(b), "Green max:", np.max(g), "Red max:", np.max(r))
        print(np.max(b), np.max(g), np.max(r))

    if np.average([b, g, r]) > beltThreshold:
        if color_counter == 0:
            yellow.append([b, g, r])
        elif color_counter == 1:
            orange.append([b, g, r])
        elif color_counter == 2:
            red.append([b, g, r])
        elif color_counter == 3:
            green.append([b, g, r])
        else:
            pass

    cv.imshow('monk', frame)

yellow_a = np.array(yellow)
orange_a = np.array(orange)
red_a = np.array(red)
green_a = np.array(green)

print("red:", red_a)

print(f"Yellow B{yellow_a[0, :].min()},{yellow_a[0, :].max()}; G{yellow_a[1, :].min()},{yellow_a[1, :].max()}; R{yellow_a[2, :].min()},{yellow_a[2, :].max()}")
print(f"Orange B{orange_a[0, :].min()},{orange_a[0, :].max()}; G{orange_a[1, :].min()},{orange_a[1, :].max()}; R{orange_a[2, :].min()},{orange_a[2, :].max()}")
print(f"Red B{red_a[0, :].min()},{red_a[0, :].max()}; G{red_a[1, :].min()},{red_a[1, :].max()}; R{red_a[2, :].min()},{red_a[2, :].max()}")
print(f"Green B{green_a[0, :].min()},{green_a[0, :].max()}; G{green_a[1, :].min()},{green_a[1, :].max()}; R{green_a[2, :].min()},{green_a[2, :].max()}")
