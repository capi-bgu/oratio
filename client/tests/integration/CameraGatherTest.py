import os
import time
import pathlib
import unittest

import cv2

from tests.SessionStub import SessionStub
from src.collection.CameraCollector import CameraCollector
from src.processing.CameraProcessor import CameraProcessor

class CameraGatherTest(unittest.TestCase):
    def test(self):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/img"):
            os.mkdir("../test_output/img")
        self.out_path = os.path.join(test_dir, 'test_output', 'img')
        fps = 2

        camera_processor = CameraProcessor()
        camera_collector = CameraCollector(fps)

        st = time.time()
        session = SessionStub(1, 5, st)

        st = time.time()
        camera_collector.start()
        time.sleep(session.session_duration)
        data = camera_collector.stop_collect()
        camera_collector.join()
        print(time.time() - st)

        st = time.time()
        camera_processor.set_arguements(data, session)
        camera_processor.start()
        camera_processor.join()
        features = camera_processor.features
        print(time.time() - st)

        for i, img in enumerate(features):
            cv2.imwrite(f"{self.out_path}\\integration_test_{i}.jpg", img)

if __name__ == '__main__':
    unittest.main()
