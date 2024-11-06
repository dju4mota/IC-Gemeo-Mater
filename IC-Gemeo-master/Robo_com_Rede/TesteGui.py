import cv2
import numpy as np

from Sockets.client import Client
from ultralytics import YOLO

model = YOLO("../../runs/detect/train20/weights/best.pt")

cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

# centro = [640, 360]
centro = [618, 317]
coordenadas = [0, 0]


def get_proportionality(image: str = IMAGE, model: str = MODEL_TABLE) -> Tuple[float, float]:
    # Inferência
    model = YOLO(model)
    results = model(image)
    xyxy = results[0].boxes.xyxy

    # Frames
    for index, box in enumerate(xyxy):
        frame = Frame.yolov8_infer(box, prefix='table')
        frame.name = f"table_{index}"

    # Calculate the proportionality
    p_distance_width = Frame.get_distance((frame.coords[0][0], frame.coords[0][1]),
                                          (frame.coords[1][0], frame.coords[1][1]))
    p_distance_height = Frame.get_distance((frame.coords[0][0], frame.coords[0][1]),
                                           (frame.coords[3][0], frame.coords[3][1]))

    prop_width = TABLE_WIDTH_ON_MM / p_distance_width
    prop_height = TABLE_HEIGHT_ON_MM / p_distance_height
    average = (prop_width + prop_height) / 2

    return {
        'width_pixels': p_distance_width,
        'height_pixels': p_distance_height,
        'width_mm': p_distance_width * average,
        'height_mm': p_distance_height * average,
        'average': average
    }

def move_robo(x, y):
    cliente = Client()
    cliente.send_message(f"GX{x}Y{y}E")
    cliente.close_connection()

def distancia_media(img):
    print(f"Centro: {centro}")
    results = model(img)

    for result in results:
        # result.show()
        pos = result.boxes.numpy().xyxy

        result_img = cv2.circle(img, (x, y), radius=3, color=(0, 255, 0), thickness=-1)
        cv2.imshow("peca", result_img)
        x = x - centro[0]
        # eixo Y da camera e do robo são invertidos
        y = -y + centro[1]
        print(f"x: {x}")
        print(f"y: {y}")

        print("regressao linear")
        # x, y = corrige_medidas(x, y)
        # x = round(x)
        # y = round(y)
        # print(f"x: {x}")
        # print(f"y: {y}")

        # move_robo(x, y)
        global coordenadas
        coordenadas = [x, y]

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

    # elif k % 256 == 99:
    #     # C pressed
    #     calibra_centro_da_mesa(frame)

    elif k % 256 == 116:
        # T pressed
        move_robo(coordenadas[0], coordenadas[1])

    elif k % 256 == 32:
        # SPACE pressed
        try:
            distancia_media(frame)
            #img = corrige_distorcao(frame,matriz,coeficiente)
            #distancia_media(img)
        except Exception as e:
            print("erro para calcular distancia")
            print(e)

cam.release()
cv2.destroyAllWindows()