import cv2
from Sockets.client import Client
from ultralytics import YOLO


def calcula_centro_da_peca(pos):
    x = round((pos[0][0] + pos[0][2]) / 2)
    y = round((pos[0][1] + pos[0][3]) / 2)
    return x, y


def move_robo(x, y):
    cliente = Client()
    cliente.send_message(f"GX{x}Y{y}E")
    cliente.close_connection()


def calibra_centro_da_mesa(img):
    results = model(img)

    pos = results[0].boxes.numpy().xyxy
    x, y = calcula_centro_da_peca(pos)

    global centro
    centro = [x, y]
    print(f"fCentro encontrado: {centro}")


def distancia_media(img):
    print(f"fCentro encontrado: {centro}")
    results = model(img)

    for result in results:
        # result.show()
        pos = result.boxes.numpy().xyxy
        x, y = calcula_centro_da_peca(pos)

        x = x - centro[0]
        y = -y + centro[1]

        print(x)
        print(y)

        move_robo(x, y)


model = YOLO("../../runs/detect/train20/weights/best.pt")

cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

# atualmente centro está hardcoded e estático, precisamos de uma etapa de calibragem ou manual ou por software
centro = [640, 360]

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

    elif k % 256 == 99:
        # C pressed
        calibra_centro_da_mesa(frame)

    elif k % 256 == 116:
        # T pressed
        move_robo(100, 100)

    elif k % 256 == 32:
        # SPACE pressed
        try:
            distancia_media(frame)
        except:
            print("erro para calcular distancia")


cam.release()
cv2.destroyAllWindows()

