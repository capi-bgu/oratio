import cv2
import time
import logging
from src.collection.DataCollector import DataCollector


class CameraCollector(DataCollector):
    def __init__(self, fps, camera):
        super().__init__()
        self.fps = fps
        self.camera = camera
        self.cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

    def start_collect(self):
        logging.info("start camera collecting...")
        super().start_collect()
        while self.collect:
            _, frame = self.cap.read()
            if frame is not None:
                self.data.append(frame)
            time.sleep(1.0 / self.fps)
        logging.info("end camera collecting...")

    def stop_collect(self):
        # self.cap.release()
        return super().stop_collect()
