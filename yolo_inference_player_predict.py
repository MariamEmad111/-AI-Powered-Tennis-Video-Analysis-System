from ultralytics import YOLO
model = YOLO('yolov8x')  # load a pretrained model (recommended for training)
result = model.predict(r"input_videos\input_video.mp4", save=True)
print(result)
print("boxes:")
    
for box in  result[0].boxes:
    print(box)