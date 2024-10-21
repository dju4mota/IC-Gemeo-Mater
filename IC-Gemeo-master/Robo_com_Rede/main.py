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
    result_img = cv2.circle(img, (x, y), radius=10, color=(0, 255, 0), thickness=-1)
    cv2.imshow("centro calibrado", result_img)

    global centro
    centro = [x, y]
    print(f"fCentro encontrado: {centro}")


def distancia_media(img):
    print(f"Centro: {centro}")
    results = model(img)

    for result in results:
        # result.show()
        pos = result.boxes.numpy().xyxy
        x, y = calcula_centro_da_peca(pos)
        x = x - centro[0]
        # eixo Y da camera e do robo são invertidos
        y = -y + centro[1]

        print(f"x: {x}")
        print(f"y: {y}")

        # move_robo(x, y)
        global coordenadas
        coordenadas = [x, y]


model = YOLO("../../runs/detect/train20/weights/best.pt")

cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

# centro = [640, 360]
centro = [618, 317]
coordenadas = [0, 0]

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
        move_robo(coordenadas[0], coordenadas[1])

    elif k % 256 == 32:
        # SPACE pressed
        try:
            distancia_media(frame)
        except:
            print("erro para calcular distancia")


cam.release()
cv2.destroyAllWindows()

