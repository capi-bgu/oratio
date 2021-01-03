import os

import cv2
from src.processing.DataProcessor import DataProcessor
import pathlib


class CameraProcessorStub(DataProcessor):
    def __init__(self):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        output_path = os.path.join(test_dir, 'test_output', 'img')
        super().__init__(output_path=output_path)

    def process_data(self, data, session):
        for i, pic in enumerate(data):
            cv2.imwrite(str(session.session_name)+'_'+str(i) + ".jpg", pic)
