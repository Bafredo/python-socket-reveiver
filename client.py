import cv2

cap = cv2.VideoCapture()
while True:
    ret,f = cap.read()
    if ret:
        cv2.imshow("camera feed",f)
        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()