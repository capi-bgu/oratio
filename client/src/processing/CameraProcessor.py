from src.processing.DataProcessor import DataProcessor
import numpy as np
import dlib
import cv2
import pathlib
import os


class CameraProcessor(DataProcessor):
    def __init__(self, output_path):
        super().__init__(output_path)

        processing_dir = pathlib.Path(__file__).parent.absolute()
        self.predictor_path = os.path.join(processing_dir, 'dlib_face_detection.dat')
        self.predictor = dlib.shape_predictor(self.predictor_path)
        self.detector = dlib.get_frontal_face_detector()

    def process_data(self, data, session):
        super().process_data(data, session)
        for i, frame in enumerate(data):
            frame = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)
            frame = frame/255.0
            frame = cv2.pow(frame, 0.6)
            frame = frame*255
            frame = frame.astype(np.uint8)

            faces = self.detector(frame)
            for face in faces:
                # Create landmark object
                landmarks = self.predictor(image=frame, box=face)

                x = []; y = []
                for n in range(0, 68):
                    x.append(landmarks.part(n).x)
                    y.append(landmarks.part(n).y)
                cut_frame = frame[min(y):max(y), min(x):max(x)]
                cv2.imwrite(f"{self.output_path}\\s_{session.session_name}_pn_{i}.jpg", cut_frame)


