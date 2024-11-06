import cv2
import numpy as np

from Sockets.client import Client
from ultralytics import YOLO

from sklearn.linear_model import LinearRegression

# Dados medidos (capturados pela câmera) e reais (medidos manualmente)
medidas_camera = np.array([
    [0, 0], [0, 2.7], [0.1, 4.4], [0, 7.2], [0.1, 9], [0, 11.6], [0, 13.3],
    [-1.7, 0.1], [-1.6, 2.7], [-1.7, 4.5], [-1.6, 7.2], [-1.6, 8.9],
    [-1.6, 11.5], [-1.5, 13.3], [-4.2, 0.2], [-4.3, 2.7], [-4.3, 4.5],
    [-4.2, 7.2], [-4.2, 9], [-4.2, 11.6], [-4.1, 13.4], [-6, 0.2],
    # Adicione todas as suas medidas capturadas pela câmera
])

medidas_reais = np.array([
    [0, 0], [0, 3], [0, 5], [0, 8], [0, 10], [0, 13], [0, 15],
    [-2, 0], [-2, 3], [-2, 5], [-2, 8], [-2, 10],
    [-2, 13], [-2, 15], [-5, 0], [-5, 3], [-5, 5],
    [-5, 8], [-5, 10], [-5, 13], [-5, 15], [-7, 0],
    # Adicione todas as suas medidas reais
])

# Ajustar um modelo de regressão linear para cada eixo
# reg_x = LinearRegression().fit(medidas_camera[:, 0].reshape(-1, 1), medidas_reais[:, 0])
# reg_y = LinearRegression().fit(medidas_camera[:, 1].reshape(-1, 1), medidas_reais[:, 1])

# Função para corrigir a distorção das medidas capturadas
# def corrige_medidas(x_camera, y_camera):
#     x_real = reg_x.predict(np.array([[x_camera]]))[0]
#     y_real = reg_y.predict(np.array([[y_camera]]))[0]
#     return x_real, y_real


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
    result_img = cv2.circle(img, (x, y), radius=3, color=(0, 255, 0), thickness=-1)
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

matriz = [[4.92293033e+03, 0.00000000e+00, 7.42347382e+02],
 [0.00000000e+00, 5.13248071e+03, 3.35363447e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
matriz = np.array(matriz)
coeficiente = [[-1.09545866e+01,  1.00563150e+03,  2.38253511e-02, -1.56173609e-01,
   8.68376105e+00]]
coeficiente = np.array(coeficiente)

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
            #img = corrige_distorcao(frame,matriz,coeficiente)
            #distancia_media(img)
        except Exception as e:
            print("erro para calcular distancia")
            print(e)

cam.release()
cv2.destroyAllWindows()
