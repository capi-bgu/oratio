import os
import cv2
import time
import pathlib
import unittest
from src.collection.CameraCollector import CameraCollector


class CameraCollectorTest(unittest.TestCase):
    def test(self):
        self.camera_collector = CameraCollector(2)
        self.camera_collector.start()
        self.session_duration = 5
        time.sleep(self.session_duration)
        data = self.camera_collector.stop_collect()
        self.process_data(data)

    def process_data(self, data):
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/img"):
            os.mkdir("../test_output/img")
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        output_path = os.path.join(test_dir, 'test_output', 'img')
        for i, pic in enumerate(data):
            cv2.imwrite(f"{output_path}\\raw_image_{i}.jpg", pic)


if __name__ == '__main__':
    unittest.main()
