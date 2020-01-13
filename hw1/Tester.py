import imutils
import cv2

image = cv2.imread("ElderEyler.jpeg")

(h, w, d) = image.shape
print(f"width: {w}, height: {h}, depth:{d}")

(B,G,R) = image[100,50]
print(f"R: {R}, G: {G}, B: {B}")

# cv2.imshow("Image", image)
# cv2.waitKey(0)

roi = image[90:220, 250:360]

# cv2.imshow("Eyler", roi)
# cv2.waitKey(0)

resized = cv2.resize(image, (int(w/2),int(h)))
cv2.imshow("Resized", resized)
cv2.waitKey(0)
