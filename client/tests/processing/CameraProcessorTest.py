import os
from concurrent.futures._base import as_completed

import cv2
import time
import pathlib
import unittest
from os import listdir
from os.path import isfile, join
from tests.SessionStub import SessionStub
from src.processing.CameraProcessor import CameraProcessor

class CameraProcessorTest(unittest.TestCase):
    def test(self):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/img"):
            os.mkdir("../test_output/img")
        self.out_path = os.path.join(test_dir, 'test_output', 'img')
        self.data_path = os.path.join(test_dir, 'test_data', 'img')
        self.cpt = CameraProcessor()
        session_duration = 5
        data = self.__get_data()

        st = time.time()
        session = SessionStub(0, session_duration, st)
        self.cpt.set_arguements(data, session)
        self.cpt.start()
        self.cpt.join()
        features = self.cpt.features
        print(time.time()-st)

        for i, img in enumerate(features):
            cv2.imwrite(f"{self.out_path}\\processor_test_{i}.jpg", img)

    def __get_data(self):
        data = []
        self.files = [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]
        for img in self.files:
            data.append(cv2.imread(self.data_path + '\\' + img))
        return data


if __name__ == '__main__':
    unittest.main()
