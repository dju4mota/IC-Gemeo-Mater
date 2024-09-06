import json
import math
import os.path
import shutil

import numpy
from ultralytics import YOLO
from ultralytics.solutions import distance_calculation
import cv2
from datetime import datetime


#  results = model.predict("../imagens/ic-basico.v4i.yolov8-obb/test/images/WIN_20240326_16_06_12_Pro_jpg.rf"
#                        ".dbe0fde910d83e12284a6d86ae6d5342.jpg")
#  results = model.predict("../imagens/camera_nova/WIN_20240318_20_20_30_Pro.jpg")


def calcular_distancia(pixel_per_meter, centroid1, centroid2):
    pixel_distance = math.sqrt((centroid1[0] - centroid2[0]) ** 2 + (centroid1[1] - centroid2[1]) ** 2)
    return pixel_distance / pixel_per_meter * 100


def gerarLog(filename, distance, foto, predict):
    info = {
        "foto": foto,
        "predict": predict,
        "distancia-calculada": distance,
    }

    with open(filename, "r+") as json_file:
        # First we load existing data into a dict.
        file_data = json.load(json_file)
        # Join new_data with file_data inside emp_details
        file_data["testes"].append(info)
        # Sets file's current position at offset.
        json_file.seek(0)
        # convert back to json.
        json.dump(file_data, json_file, indent=4)


def salva_imagem_predict(pontoX, pontoY):
    print((pontoX, pontoY))
    pontoX = int(pontoX)
    pontoY = int(pontoY)
    result_img = cv2.imread("C:\\Code\\Projetinhos\\IC-Gemeo-master\\runs\\detect\\predict\\image0.jpg")
    result_img = cv2.circle(result_img, (pontoX,  pontoY), radius=10, color=(0,255,0),thickness=-1)
    save_img = "foto_predict_" + datetime.now().strftime("%H-%M-%S") + ".png"
    path = 'C:\\Code\\Projetinhos\\IC-Gemeo-master\\IC-Gemeo-master\\Localização de Objetos - Mesa Real\\testes'
    cv2.imwrite(os.path.join(path, save_img), result_img)
    return save_img


def distancia_media(img):
    media_distancia = 0
    quantidade = 1
    for i in range(0, quantidade):
        results = model(img)
        centroids = []
        for result in results:
            #result.show()
            for pos in result.boxes.numpy().xyxy:
                centroids.append(pos)

        dist_obj = distance_calculation.DistanceCalculation()
        dist_obj.pixel_per_meter = 870
        #centro da imagem
        #centro = numpy.asarray([640, 360, 641, 361])
        distance = dist_obj.calculate_distance(centroids[0], centroids[1])

        result_img = cv2.circle(img, (int(centroids[0][0]), int(centroids[0][1])), radius=10, color=(0, 255, 0), thickness=-1)
        #result_img = cv2.circle(result_img, (640, 360), radius=10, color=(0, 255, 0), thickness=-1)
        result_img = cv2.circle(img, (int(centroids[1][0]), int(centroids[1][1])), radius=10, color=(0, 255, 0), thickness=-1)
        cv2.imshow("distancia", result_img)

        media_distancia += distance[1]
    print(f"final: {media_distancia/quantidade}")



def distancia(img, logFilename, img_name):
    # img = cv2.resize(img, (640, 640))
    results = model(img, save=True)

    centroids = []
    #  print(results)
    dist_obj = distance_calculation.DistanceCalculation()

    for result in results:
        result.show()
        # print(result.boxes)
        # centroids.append(dist_obj.calculate_centroid(result.boxes))
        # dist_obj.start_process()
        for pos in result.boxes.numpy().xyxy:
            print(pos)
            centroids.append(pos)

    # 578 com pre processamento
    # 1153 direto do opencv

    # 29 de altura:
    # 883  (1 m)
    # 870 (10 cm)
    # 8.7

    #58 cm de altura (peso embaixo da mesa ao começo da base de ferro)
    # 500 - 60
    # 8.3 - 1
    dist_obj.pixel_per_meter = 830
    distance = dist_obj.calculate_distance(centroids[0], centroids[1])
    print(distance)
    print(centroids[0])
    print(centroids[1])
    #print(calcular_distancia(1153, centroids[0], centroids[1]))
    # predict_name = salva_imagem_predict(centroids[1][0], centroids[1][1])
    #try:
     #   gerarLog(logFilename, distance, img_name, predict_name)
    #except:
    #    print("erro gerar log")


# Yolo
model = YOLO("../../runs/detect/train20/weights/best.pt")
# Open CV
height = 720
width = 1280
cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
img_counter = 0

# Logs dos testes
try:
    shutil.rmtree("C:\\Code\\Projetinhos\\IC-Gemeo-master\\runs\\detect\\predict")
except:
    print("erro deletar predict")
logFilename = ".\\testes\\log_" + datetime.now().strftime("%H-%M-%S") + ".json"
with open(logFilename, "w") as json_file:
    t = {"testes": []}
    json.dump(t, json_file, indent=4)

while True:
    ret, frame = cam.read()
    # frame = cv2.imread("C:\\Code\\Projetinhos\\IC-Gemeo-master\\IC-Gemeo-master\\Localização de Objetos - Mesa Real\\testes\\foto_live_16-57-10.png")
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
        img_name = "foto_live_" + datetime.now().strftime("%H-%M-%S") + ".png"
        path = 'C:\\Code\\Projetinhos\\IC-Gemeo-master\\IC-Gemeo-master\\Localização de Objetos - Mesa Real\\testes'
        cv2.imwrite(os.path.join(path, img_name), frame)
        img_counter += 1
        try:
            #distancia(frame, logFilename, img_name)
            distancia_media(frame)
        except:
            print("erro para calcular distancia")

cam.release()
cv2.destroyAllWindows()


#  pixel vs milimitro
#  distorção da camera ( meio pras borodas) parallax
#  * grid de calibração
# converter pixel em milimetro
# plano invertido para camera
# origem em comum

# comunicação
# socket TCP
# fazer algum tipo de protocolo
# rasberry socket server
# robo socket client
# robo manda um flag
# rasberry manda target até ser lido


# aplicaçao do staubli
# cria world -> frame
# socket client
# criar sio -> linka com o socket
# precisam se conversar para setar o frame e a origem, vai ser a base


# iluminação !!!
# frequencia da lampada
# contraste
