import os
import cv2
import pathlib
from os import listdir
from os.path import isfile, join
from src.collection.DataCollector import DataCollector


class CameraCollectorStub(DataCollector):
    def __init__(self, fps=2, camera=0):
        super().__init__()
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.data_path = os.path.join(test_dir, 'test_data', 'img', 'raw_data')
        self.fps = fps

    def start_collect(self):
        pass

    def stop_collect(self):
        data = []
        files = [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]
        for img in files:
            data.append(cv2.imread(self.data_path + '\\' + img))
        return data


if __name__ == '__main__':
    camera_collector_stub = CameraCollectorStub()
    data = camera_collector_stub.stop_collect()
    print(data)
