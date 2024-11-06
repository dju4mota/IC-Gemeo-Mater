from CONSTANTES import LOGS
from classes.Cam.cam import CameraApp
from classes.Network.client import Client
from classes.frame.frame import Frame, IMAGE, MODEL_BLOCKS, MODEL_TABLE

cam = CameraApp()
cam.capture_snapshot()
cam.close()

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
    print(f"{LOGS['CONNECT']} {block}")
    socket_client = Client()
    socket_client.connect_to_server()
    valor = block['y_mm']  # Substituir isso pela manipulação adequada se for uma série
    
    message = f"GX{round(block['x_mm'])}Y{round(block['y_mm'])}E"
    print(message)
    socket_client.send_message(message)