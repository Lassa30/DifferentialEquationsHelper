import os
import sys

# The script takes only one argument - path:
#   path = path to the folder that stores the data in YOLO format.

path = sys.argv[1]
images_path = "images"
labels_path = "labels"

for suffix in ["train", "val"]:
    for image_path_with_ext in os.listdir(os.path.join(path, images_path, suffix)):
        image_path_without_ext = image_path_with_ext.split(".")[0]

        label_file_path = os.path.join(path, labels_path, suffix, image_path_without_ext + ".txt")
        if not (os.path.isfile(label_file_path)):
            open(label_file_path, "a").close()
            print(f"label for file: {label_file_path}\n\t- is created")
