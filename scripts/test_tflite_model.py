import os
from ultralytics import YOLO

model = YOLO("../models/yolo_detection.tflite", task="detect")

test_root = "../data/test"
test_images = [os.path.join(test_root, filename) for filename in os.listdir(test_root)]

for ind, image in enumerate(test_images):
    result = model(image)[0]
    result.save(filename=f"../test_results/res_{ind}.png")
