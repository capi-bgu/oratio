import time
import logging
import unittest
from threading import Thread
from tests.SessionStub import SessionStub
from oratio.processing.CameraProcessor import CameraProcessor
from tests.collection.stubs.CameraCollectorStub import CameraCollectorStub
from tests.database.sqlite_db.stubs.CameraDataHandlerStub import CameraDataHandlerStub


class CameraProcessorTest(unittest.TestCase):
    def test(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        camera_collector = CameraCollectorStub()
        camera_collector.start_collect()
        data = camera_collector.stop_collect()

        self.camera_processor = CameraProcessor()
        session_duration = 5
        st = time.time()
        session = SessionStub("CameraProcessingTest", session_duration, st)
        processor = Thread(target=self.camera_processor.process_data, args=(data, session))
        processor.start()
        processor.join()
        features = self.camera_processor.features
        logging.debug(time.time() - st)

        self.assertTrue(len(features) == session.duration * camera_collector.fps)
        for img in features:
            self.assertTrue(img.shape == (150, 150))

        data_handler = CameraDataHandlerStub(name="processed")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()
