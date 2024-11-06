from frame import Frame,IMAGE, MODEL_BLOCKS, MODEL_TABLE

import cv2

from Sockets.client import Client
from ultralytics import YOLO


def fazTudo():
    table_frames = Frame.infer_frames(IMAGE, MODEL_TABLE, 'table')
    blocks_frames = Frame.infer_frames(IMAGE, MODEL_BLOCKS, 'blocks')
    reason_pixels_mm = Frame.get_proportionality()

    Frame.draw_frames(blocks_frames, table_frames[0], True, IMAGE, 'result.png', reason_pixels_mm['average'])

    blocks = []

    for frame in blocks_frames:
        coords = Frame.get_coords(table_frames[0], frame, reason_pixels_mm['average'])
        # validar se nao é a origem
        # validar se nao está fora da mesa branca
        if(coords['x_mm'] == 0 and coords['y_mm'] == 0):
            continue
        if(coords['x_mm'] > 300 or coords['y_mm'] > 300 or coords['x_mm'] < -300 or coords['y_mm'] < -300):
            continue
        blocks.append(coords)

    for block in blocks:
        socket_client = Client()
        socket_client.connect_to_server()
        valor = block['y_mm']  # Substituir isso pela manipulação adequada se for uma série

        message = f"GX{round(block['x_mm'])}Y{round(block['y_mm'])}E"
        print(message)
        socket_client.send_message(message)


def move_robo(x, y):
    cliente = Client()
    cliente.send_message(f"GX{x}Y{y}E")
    cliente.close_connection()


cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)


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

    # elif k % 256 == 116:
    #     # T pressed
    #     move_robo(coordenadas[0], coordenadas[1])

    elif k % 256 == 32:
        # SPACE pressed
        cv2.imwrite("./images/image.png", frame)
        fazTudo()

cam.release()
cv2.destroyAllWindows()
