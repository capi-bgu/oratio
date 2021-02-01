import time
import unittest
from threading import Thread
from tests.SessionStub import SessionStub
from src.collection.CameraCollector import CameraCollector
from src.processing.CameraProcessor import CameraProcessor
from tests.database.sqlite_db.stubs.CameraDataHandlerStub import CameraDataHandlerStub


class CameraTest(unittest.TestCase):
    def test(self):
        fps = 2
        camera = 0
        self.camera_processor = CameraProcessor()
        self.camera_collector = CameraCollector(fps, camera)

        st = time.time()
        session = SessionStub("CameraCollectingProcessingTest", 5, st)

        # collecting
        st = time.time()
        collector = Thread(target=self.camera_collector.start_collect)
        collector.start()
        time.sleep(session.duration)
        data = self.camera_collector.stop_collect()
        collector.join()
        print(time.time() - st)

        # processing
        st = time.time()
        processor = Thread(target=self.camera_processor.process_data, args=(data, session))
        processor.start()
        processor.join()
        features = self.camera_processor.features
        print(time.time() - st)
        self.assertLessEqual(len(features), session.duration * self.camera_collector.fps)
        for img in features:
            self.assertTupleEqual(img.shape, (150, 150))

        # database
        data_handler = CameraDataHandlerStub(name="gathered")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()
