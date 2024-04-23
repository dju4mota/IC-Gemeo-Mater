from ultralytics import YOLO


#model = YOLO('yolov8n-obb.yaml')

model = YOLO("yolov8n.yaml")
#model = YOLO("yolov8n.pt")
# model = YOLO('yolov8n-obb.yaml')


results = model.train(data="config.yaml", epochs=200)
