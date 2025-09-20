from ultralytics import YOLO

model = YOLO("bee_cam/bombusvaledit_11s_0012/weights/bombusvaledit_11s_001.pt")

model.export(format="onnx")
