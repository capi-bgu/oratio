import os
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

        self.out_path = os.path.join(test_dir, 'test_output')
        self.data_path = os.path.join(test_dir, 'test_data', 'img')
        self.cpt = CameraProcessor(self.out_path)
        data = self.__get_data()
        st = time.time()
        self.cpt.process_data(data, SessionStub(0, 5, st))
        print(time.time()-st)

    def __get_data(self):
        data = []
        self.files = [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]
        for img in self.files:
            data.append(cv2.imread(self.data_path + '\\' + img))

        return data


if __name__ == '__main__':
    unittest.main()
