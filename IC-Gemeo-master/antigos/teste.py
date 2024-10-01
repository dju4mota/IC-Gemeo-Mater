import cv2

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)


ret, frame = cam.read()


while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed
        try:
            result_img = cv2.circle(frame, (0, 0), radius=10, color=(0, 255, 0), thickness=-1)
            cv2.imshow("distancia", result_img)
        except:
            print("erro para calcular distancia")


cam.release()
cv2.destroyAllWindows()

