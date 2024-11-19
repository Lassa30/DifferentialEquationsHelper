import pymupdf
from PIL import Image
import pyheif
import os
import pandas as pd
import shutil
from sklearn.model_selection import train_test_split
import cv2


def pdf_pages_to_images(pdf_input_path, images_output_path, logging=False):
    if not (os.path.isdir(pdf_input_path) and os.path.isdir(images_output_path)):
        print("Check provided paths for correctness.")
        return False

    pdf_files_dir = os.listdir(pdf_input_path)
    for file in pdf_files_dir:
        images_dir = images_output_path

        if not os.path.isdir(images_dir):
            os.mkdir(images_dir)

        doc_path = pdf_input_path + f"/{file}"
        document = pymupdf.open(doc_path)
        pictures_counter = 0
        for page in document:
            picture = page.get_pixmap()
            picture.save("{}/{}-page-{}.png".format(images_dir, file.split(".")[0], page.number + 1))
            pictures_counter += 1
        print("pdf_pages_to_images: {} is done.\n{} images are saved in total.".format(file, pictures_counter))

    return True


def video_to_frames(video, path_output_dir, video_name):
    vid = cv2.VideoCapture(video)
    count = 1
    while vid.isOpened():
        success, image = vid.read()
        if success:
            if count % 120 == 0:
                image_name = "{}_{}.png".format(video_name, count)
                cv2.imwrite(os.path.join(path_output_dir, image_name), image)
        else:
            break
        count += 1
    cv2.destroyAllWindows()
    vid.release()


def heic_to_jpeg(images_input_path, delete_heic=False):
    if not os.path.isdir(images_input_path):
        print("heic_to_jpeg: wrong images_input_path:\n\t{}".format(images_input_path))
        return False

    heic_files = [f for f in os.listdir(images_input_path) if f.lower().endswith(".heic")]
    if not heic_files:
        print("heic_to_jpeg: No HEIC files found.")
        return True

    for heic_file in heic_files:
        heic_path = os.path.join(images_input_path, heic_file)
        jpg_path = os.path.join(images_input_path, f"{os.path.splitext(heic_file)[0]}.jpg")

        try:
            heif_file = pyheif.read(heic_path)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
            image.save(jpg_path, "JPEG")
            print(f"heic_to_jpeg: Converted \n\t{heic_file}\nto\n\t{jpg_path} successfully.")

            if delete_heic and os.path.exists(heic_path):
                os.remove(heic_path)

        except Exception as e:
            print(f"heic_to_jpeg: Failed to convert {heic_file}. Error: {str(e)}")

    return True


class DataFrameFromImages:
    """
    Class to get pandas.DataFrame from images.
    
    Also it's possible to split data to train and val in given proportion, If you have dataframe.
    If the labels are provided, stratification is applied.
    Otherwise just random split of images is applied.
    """

    def __init__(self, images_dataframe=None, dir_path="../data", images_dir_name="images/images_all", labels_dir_name="labels/labels_all"):
        self.dir_path = dir_path
        self.images_dir_name = images_dir_name
        self.labels_dir_name = labels_dir_name
        self.images_dataframe = images_dataframe

    def create_dataframe(self):
        # labels and images have the same root directory: for example ../data
        path = os.path.join(self.dir_path)
        images_path = os.path.join(path, self.images_dir_name)
        labels_path = os.path.join(path, self.labels_dir_name)

        if not all((os.path.isdir(path), os.path.isdir(images_path), os.path.isdir(labels_path))):
            print(
                "create_dataframe: one of provided paths:\n{}\n{}\n{}\n - is not valid.".format(
                    path, images_path, labels_path
                )
            )
            return None

        images_files = [f for f in os.listdir(images_path) if not os.path.isdir(os.path.join(images_path, f))]
        labels_files = [f[:-5] for f in os.listdir(labels_path) if not os.path.isdir(os.path.join(images_path, f))]
        has_label = [
            1 if f.rsplit(".", 1)[0] in set(labels_files) else 0
            for f in os.listdir(images_path)
            if not os.path.isdir(os.path.join(images_path, f))
        ]

        labels_files = [f for f in os.listdir(labels_path)]

        try:
            df = pd.DataFrame({"img_name": images_files, "label": has_label})
            self.images_dataframe = df
            return self
        except:
            return None

    def copy_to_postfix_dir(self, source_files_df, images_path, labels_path, postfix):
        for ind in range(len(source_files_df)):
            train_image = source_files_df.iloc[ind].to_numpy()
            has_label = train_image[1]

            copy_image_from = os.path.join(images_path, train_image[0])
            copy_image_to = os.path.join(images_path, postfix, train_image[0])
            try:
                shutil.copy(copy_image_from, copy_image_to)
            except Exception as e:
                print("Image copy.\n")
                print("\nException occured: {}\n".format(e))

            if has_label:
                copy_from = os.path.join(os.path.join(labels_path, train_image[0].rsplit(".", 1)[0] + ".json"))
                copy_to = os.path.join(labels_path, postfix, train_image[0].rsplit(".", 1)[0] + ".json")
                try:
                    shutil.copy(copy_from, copy_to)
                except Exception as e:
                    print("\nException occured: {}\n".format(e))

    def train_test_folder(self, train_size=0.8, stratify=None):
        if self.images_dataframe is None:
            print("train_test_folder: \nFirstly, create a dataframe.")
            return False

        train_images_df, val_images_df = train_test_split(
            self.images_dataframe,
            train_size=train_size,
            stratify=stratify,
            shuffle=True,
            random_state=42,
        )

        images_path = os.path.join(self.dir_path, self.images_dir_name)
        labels_path = os.path.join(self.dir_path, self.labels_dir_name)

        try:
            self.copy_to_postfix_dir(
                source_files_df=train_images_df, images_path=images_path, labels_path=labels_path, postfix="train"
            )
            self.copy_to_postfix_dir(
                source_files_df=val_images_df, images_path=images_path, labels_path=labels_path, postfix="val"
            )
        except Exception as e:
            print("Exception: {}".format(e))

        return True
