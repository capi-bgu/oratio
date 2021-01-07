import cv2
import time
from src.collection.DataCollector import DataCollector


class CameraCollector(DataCollector):
    def __init__(self, fps=2, camera=0):
        super().__init__()
        self.fps = fps
        self.cap = cv2.VideoCapture(camera)

    def start_collect(self):
        print("start camera collecting...")
        super().start_collect()
        prev = 0
        while self.collect:
            time_elapsed = time.time() - prev
            if time_elapsed > 1. / self.fps:
                prev = time.time()
                _, frame = self.cap.read()
                if frame is not None:
                    self.data.append(frame)
        print("end camera collecting...")

    def stop_collect(self):
        self.cap.release()
        return super().stop_collect()
