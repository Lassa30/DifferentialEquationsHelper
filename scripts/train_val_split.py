from image_preparation import DataFrameFromImages

if __name__ == "__main__":
    data_splitter = DataFrameFromImages(
        dir_path="../data", images_dir_name="images", labels_dir_name="labels"
    )

    data_splitter.create_dataframe().train_test_folder(train_size=0.8)
