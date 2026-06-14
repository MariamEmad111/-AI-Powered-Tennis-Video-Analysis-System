from ultralytics import YOLO
model = YOLO('Models/last.pt')  # load a pretrained model (recommended for training)
result = model.predict(r"input_videos\input_video.mp4",conf=0.2, save=True)
print(result)
print("boxes:")
    
for box in  result[0].boxes:
    print(box)