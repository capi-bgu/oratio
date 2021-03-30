import cv2
import time
import logging
from oratio.collection.DataCollector import DataCollector
from threading import Condition, Lock


class CameraCollector(DataCollector):
    def __init__(self, fps, camera):
        super().__init__()
        self.fps = fps
        self.camera = camera
        self.cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        self.waiter = Condition(Lock())
        self.spf = 1.0 / fps

    def start_collect(self):
        logging.info("start camera collecting...")
        self.waiter.acquire(True)
        super().start_collect()
        while self.collect:
            _, frame = self.cap.read()
            if frame is not None:
                self.data.append(frame)
            self.waiter.wait(self.spf)
            # time.sleep(1.0 / self.fps)
        self.waiter.release()
        logging.info("end camera collecting...")

    def stop_collect(self):
        # self.cap.release()
        self.waiter.acquire(True)
        data = super().stop_collect()
        self.waiter.notify()
        self.waiter.release()
        return data
