import os
from image_preparation import video_to_frames

if __name__ == "__main__":
    flag = input("Do you want to extract images from videos (1/0)?\n>>> ")
    if flag == "1":
        videos_path = "../data/videos"
        images_path = "../data/images/images_all"
        for video_name in os.listdir(videos_path):
            video_path = os.path.join(videos_path, video_name)
            print("Video {} is processing...".format(video_name.split('.')[0]))
            video_to_frames(video_path, images_path, video_name)
            print("The end of processing.")
    else:
        print("Nothing is changed.")
