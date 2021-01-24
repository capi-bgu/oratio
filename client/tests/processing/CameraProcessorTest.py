import time
import unittest
from tests.SessionStub import SessionStub
from src.processing.CameraProcessor import CameraProcessor
from tests.collection.stubs.CameraCollectorStub import CameraCollectorStub
from tests.database.sqlite_db.stubs.CameraDataHandlerStub import CameraDataHandlerStub


class CameraProcessorTest(unittest.TestCase):
    def test(self):
        camera_collector = CameraCollectorStub()
        camera_collector.start()
        camera_collector.join()
        data = camera_collector.stop_collect()

        self.cpt = CameraProcessor()
        session_duration = 5
        st = time.time()
        session = SessionStub(0, session_duration, st)
        self.cpt.set_arguements(data, session)
        self.cpt.start()
        self.cpt.join()
        features = self.cpt.features
        print(time.time() - st)

        data_handler = CameraDataHandlerStub(name="processed")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()
