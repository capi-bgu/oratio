import os
import time
import pathlib
import unittest
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
        out_path = os.path.join(test_dir, 'test_output', 'img')


        camera_processor = CameraProcessor(out_path)
        camera_collector = CameraCollector(2)
        st = time.time()
        session = SessionStub(1, 5, st)
        camera_collector.start()
        time.sleep(session.session_duration)
        data = camera_collector.stop_collect()
        print(time.time() - st)
        st = time.time()
        camera_processor.process_data(data, session)
        print(time.time() - st)

if __name__ == '__main__':
    unittest.main()
