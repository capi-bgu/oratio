import time
import unittest
from tests.SessionStub import SessionStub
from src.collection.CameraCollector import CameraCollector
from src.processing.CameraProcessor import CameraProcessor
from tests.database.sqlite_db.stubs.CameraDataHandlerStub import CameraDataHandlerStub


class CameraTest(unittest.TestCase):
    def test(self):
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

        data_handler = CameraDataHandlerStub(name="gathered")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()
