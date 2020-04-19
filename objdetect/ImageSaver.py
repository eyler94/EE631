import cv2

cap = cv2.VideoCapture(3)


iter = 0
key='r'
while key!=ord("q"):
    _, frame = cap.read()
    cv2.imshow("frame", frame)
    key = cv2.waitKey(5) & 0xFF

    if key ==ord("c"):
        iter+=1
        print("got here")
        cv2.imwrite(f"./pic{iter}.jpg", frame)
