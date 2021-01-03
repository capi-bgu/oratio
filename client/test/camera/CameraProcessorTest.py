import cv2
import unittest
from os import listdir
from src.Session import Session
from os.path import isfile, join
from src.processing.CameraProcessor import CameraProcessor
import os
import pathlib


class CameraProcessorTest(unittest.TestCase):
    def test(self):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()

        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
            os.mkdir("../test_output/img")

        self.out_path = os.path.join(test_dir, 'test_output', 'img')
        self.data_path = os.path.join(test_dir, 'test_data', 'img')
        self.cpt = CameraProcessor(self.out_path)
        data = self.__get_data()
        self.cpt.process_data(data, Session(0, 5))

    def __get_data(self):
        data = []
        self.files = [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]
        for img in self.files:
            self.data.append(cv2.imread(self.data_path + '\\' + img))

        return data


if __name__ == '__main__':
    unittest.main()
