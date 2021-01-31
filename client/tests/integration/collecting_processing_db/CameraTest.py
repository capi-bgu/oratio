import os
import time
import pathlib
from threading import Thread

import msgpack
import unittest
import numpy as np
import msgpack_numpy as m
from tests.SessionStub import SessionStub
from src.collection.CameraCollector import CameraCollector
from src.processing.CameraProcessor import CameraProcessor
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.CameraDataHandler import CameraDataHandler


class CameraTest(unittest.TestCase):
    def test(self):
        st = time.time()
        session = SessionStub("CameraFullTest", 5, st)

        # collecting
        fps = 2
        camera = 0
        camera_collector = CameraCollector(fps, camera)
        collector = Thread(target=camera_collector.start_collect)
        st = time.time()
        collector.start()
        time.sleep(session.session_duration)
        data = camera_collector.stop_collect()
        collector.join()
        print(time.time() - st)

        # processing
        self.camera_processor = CameraProcessor()
        processor = Thread(target=self.camera_processor.process_data, args=(data, session))
        st = time.time()
        processor.start()
        processor.join()
        print(time.time() - st)

        # database
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')

        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        st = time.time()
        data_handler = CameraDataHandler(path=self.out_path)
        data_handler.create_data_holder()
        data_handler.save((session.session_name, self.camera_processor.features))
        print(time.time() - st)
        res = manager.ask(f"SELECT * FROM Camera WHERE session='{session.session_name}'")
        self.assertTrue(len(res) == 1)
        key = res[0][0]
        data = res[0][1]
        self.assertEqual(key, session.session_name)
        data = msgpack.unpackb(data, object_hook=m.decode)
        self.assertTrue(np.array_equal(data, np.array(self.camera_processor.features)))


if __name__ == '__main__':
    unittest.main()
