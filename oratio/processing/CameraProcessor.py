import os
import cv2
import dlib
import logging
import pathlib
import numpy as np
from oratio.processing.DataProcessor import DataProcessor


class CameraProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

        src_dir = pathlib.Path(__file__).parent.parent.absolute()
        self.predictor_path = os.path.join(src_dir, 'resources', 'face_detection.dat')
        self.predictor = dlib.shape_predictor(self.predictor_path)
        self.detector = dlib.get_frontal_face_detector()

    def process_data(self, data, session):
        logging.info("start camera processing...")
        self.features = []
        for i, frame in enumerate(data):
            frame = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)
            frame = frame/255.0
            frame = cv2.pow(frame, 0.6)
            frame = frame*255
            frame = frame.astype(np.uint8)

            faces = self.detector(frame)
            if len(faces) == 0:
                continue  # TODO: for future implementation- alert the user when no face detected
            elif len(faces) > 1:
                max_slant = 0
                face = 0
                for curr_index, curr_face in enumerate(faces):
                    slant = (curr_face.height()**2 + curr_face.width()**2)**0.5
                    if slant > max_slant:
                        face = curr_face
                        max_slant = slant
            else:
                face = faces[0]

            # Create landmark object
            landmarks = self.predictor(image=frame, box=face)

            x = []; y = []
            for n in range(0, 68):
                x.append(landmarks.part(n).x)
                y.append(landmarks.part(n).y)
            cut_frame = frame[min(y):max(y), min(x):max(x)]
            cut_frame = cv2.resize(cut_frame, dsize=(150, 150), interpolation=cv2.INTER_CUBIC)
            self.features.append(cut_frame)
        logging.info("end camera processing...")
        return self.features




