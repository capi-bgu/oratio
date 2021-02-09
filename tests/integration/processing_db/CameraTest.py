import os
import time
import pickle
import logging
import pathlib
import unittest
import numpy as np
from threading import Thread
from tests.SessionStub import SessionStub
from oratio.processing.CameraProcessor import CameraProcessor
from oratio.database.sqlite_db.SqliteManager import SqliteManager
from oratio.database.sqlite_db.CameraDataHandler import CameraDataHandler
from tests.collection.stubs.CameraCollectorStub import CameraCollectorStub


class CameraTest(unittest.TestCase):
    def test(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        # collecting
        camera_collector = CameraCollectorStub()
        camera_collector.start_collect()
        data = camera_collector.stop_collect()

        # processing
        self.camera_processor = CameraProcessor()
        session_duration = 5
        st = time.time()
        session = SessionStub("CameraProcessingDBTest", session_duration, st)
        processor = Thread(target=self.camera_processor.process_data, args=(data, session))
        processor.start()
        processor.join()
        logging.debug(time.time() - st)

        # database
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')

        manager = SqliteManager(path=self.out_path)
        manager.create_data_holder()

        st = time.time()
        data_handler = CameraDataHandler(path=self.out_path)
        data_handler.create_data_holder()
        data_handler.save((session.id, self.camera_processor.features))
        logging.debug(time.time() - st)
        res = manager.ask(f"SELECT * FROM Camera WHERE session='{session.id}'")
        self.assertEqual(len(res), 1)
        key = res[0][0]
        data = res[0][1]
        data = pickle.loads(data)
        self.assertEqual(key, session.id)
        self.assertEqual(len(data), len(self.camera_processor.features))
        for ret, expected in zip(data, self.camera_processor.features):
            self.assertTrue(np.array_equal(ret, expected))


if __name__ == '__main__':
    unittest.main()
