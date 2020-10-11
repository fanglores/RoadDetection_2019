import cv2

cap = cv2.VideoCapture(0)

counter = 0

while True:
    ret, img = cap.read()
    
    cv2.imshow('result', img)

    if cv2.waitKey(50) == 27:
        cv2.imwrite('photo' +  str(counter) + '.jpg', img)
        counter = counter + 1

cap.release()
cv2.DestroyAllWindows()
