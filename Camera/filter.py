import cv2
import numpy as np

image = cv2.imread('photo1.jpg')

hsv = cv2.cvtColor(image. cv2.COLOR_BGR2HSV)

cv2.imshow(hsv)

cv2.DestroyAlWindows
