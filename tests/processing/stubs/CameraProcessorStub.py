import os
import cv2
import pathlib
from os import listdir
from os.path import isfile, join
from oratio.processing.DataProcessor import DataProcessor


class CameraProcessorStub(DataProcessor):
    def __init__(self):
        super().__init__()
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.data_path = os.path.join(test_dir, 'test_data', 'img', 'processed_data')

    def process_data(self, data=None, session=None):
        features = []
        files = [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]
        for img in files:
            features.append(cv2.imread(self.data_path + '\\' + img, cv2.IMREAD_GRAYSCALE))
        self.features = features
        return self.features


if __name__ == '__main__':
    camera_processor_stub = CameraProcessorStub()
    data = camera_processor_stub.process_data()
    print(data)