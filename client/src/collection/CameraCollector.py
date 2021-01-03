from src.collection.DataCollector import DataCollector
import cv2
import time


class CameraCollector(DataCollector):
    def __init__(self, session, data_processor, fps, camera=0):
        super().__init__(session, data_processor)
        self.fps = fps
        self.cap = cv2.VideoCapture(camera)
        self.data = []

    def start_collect(self):
        self.data = []
        st = time.time()
        prev = 0
        while time.time() - self.session.session_duration < st:
            time_elapsed = time.time() - prev
            if time_elapsed > 1. / self.fps:
                prev = time.time()
                res, frame = self.cap.read()
                self.data.append(frame)
            # Exit when escape is pressed
            if cv2.waitKey(delay=1) == 27:
                break
        self.send_to_process()
        self.stop_collect()

    def stop_collect(self):
        self.cap.release()
        cv2.destroyAllWindows()
