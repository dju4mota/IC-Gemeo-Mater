from ultralytics import YOLO
from ultralytics.solutions import distance_calculation
import cv2


#  results = model.predict("../imagens/ic-basico.v4i.yolov8-obb/test/images/WIN_20240326_16_06_12_Pro_jpg.rf"
#                        ".dbe0fde910d83e12284a6d86ae6d5342.jpg")

#  results = model.predict("../imagens/camera_nova/WIN_20240318_20_20_30_Pro.jpg")


def distancia(img):
    img = cv2.resize(img, (640, 640))
    results = model.predict(img)
    centroids = []
    #  print(results)
    dist_obj = distance_calculation.DistanceCalculation()

    for result in results:
        # print(result.boxes)
        # centroids.append(dist_obj.calculate_centroid(result.boxes))
        # dist_obj.start_process()
        for pos in result.boxes.numpy().xyxy:
            print(pos)
            centroids.append(pos)

    # 11.4
    # 11.35
    # 5.78
    # esperado ~34.5 -> calculou 36.5
    # esperado ~11.5 -> calculou 11.4
    dist_obj.pixel_per_meter = 578

    print(dist_obj.calculate_distance(centroids[0], centroids[1]))


model = YOLO("../../runs/detect/train12/weights/best.pt")
cam = cv2.VideoCapture(0)
cv2.namedWindow("test")
img_counter = 0


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
        img_name = "fotos_teste_dinamico/foto-{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        img_counter += 1
        distancia(frame)

cam.release()
cv2.destroyAllWindows()


#
#
#
#
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
