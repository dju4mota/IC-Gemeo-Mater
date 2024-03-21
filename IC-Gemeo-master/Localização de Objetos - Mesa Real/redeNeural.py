from ultralytics import YOLO

model = YOLO("yolov8n.yaml")
# model = YOLO("yolov8n.pt")

results = model.train(data="config.yaml", epochs=200)



## pixel vs milimitro
## distorção da camera ( meio pras borodas) parallax
##  * grid de calibração
## converter pixel em milimetro
## plano invertido para camera
## origem em comum


## comunicação
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