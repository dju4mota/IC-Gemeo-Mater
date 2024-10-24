import cv2
import numpy as np

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


def corrige_distorcao(img, matriz_calibracao, coef_distorcao):
    h, w = img.shape[:2]
    nova_matriz_calibracao, _ = cv2.getOptimalNewCameraMatrix(matriz_calibracao, coef_distorcao, (w, h), 1, (w, h))
    img_corrigida = cv2.undistort(img, matriz_calibracao, coef_distorcao, None, nova_matriz_calibracao)
    print()
    cv2.imshow("correcao", img_corrigida)
    return img_corrigida


model = YOLO("../../runs/detect/train20/weights/best.pt")

cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

# centro = [640, 360]
centro = [618, 317]
coordenadas = [0, 0]


matriz = [[2.12774358e+03, 0.00000000e+00, 6.08343881e+02],
 [0.00000000e+00, 2.11392059e+03, 4.77682892e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
matriz = np.array(matriz)
coeficiente = [[-8.92762214e-02,  1.85631508e+01,  2.14318197e-03, -3.09855754e-03,
  -5.58801665e+02]]
coeficiente = np.array(coeficiente)



# matriz = [[2.71097975e+03, 0.00000000e+00, 6.36434420e+02],
#  [0.00000000e+00, 2.64998157e+03, 6.52368678e+02],
#  [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
# matriz = np.array(matriz)
# coeficiente = [[-4.11277456e-01,  4.80050606e-01, -6.24511506e-02,  5.74953461e-03, -5.22772668e+01]]
# coeficiente = np.array(coeficiente)


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
            img = corrige_distorcao(frame,matriz,coeficiente)
            distancia_media(img)
        except Exception as e:
            print("erro para calcular distancia")
            print(e)


cam.release()
cv2.destroyAllWindows()

