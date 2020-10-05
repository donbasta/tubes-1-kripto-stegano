import cv2 as cv
from cv2 import VideoCapture, imwrite
import os


class FrameExtractor():
    '''FrameExtractor
    Extract frames from a video into a folder.

    '''

    def __init__(self, video_path: str, save_path: str):
        self.video_path = video_path
        self.save_path = save_path
        self.load()
        print("Object handler for {} created".format(video_path))

    def load(self):
        self.vidcap = VideoCapture(self.video_path)
        print("File {} loaded".format(self.video_path))

    def extract(self):
        count = 0
        while True:
            success, image = self.vidcap.read()
            path = os.path.join(os.getcwd(), self.save_path,
                                "{:d}.png".format(count))
            if not success:
                break
            imwrite(path, image)
            print("Frame {} written to {}".format(count, path))
            count += 1

    def extract_single(self):
        if not os.path.exists(self.save_path):
            os.mkdir('temp')
        count = 0
        while count != 1:
            success, image = self.vidcap.read()
            path = os.path.join(os.getcwd(), self.save_path,
                                "{:d}.png".format(count))
            if not success:
                break
            imwrite(path, image)
            print("Frame {} written to {}".format(count, path))
            count += 1
