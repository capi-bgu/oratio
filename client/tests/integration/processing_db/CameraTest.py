import os
import time
import pathlib
import msgpack
import unittest
import numpy as np
import msgpack_numpy as m
from tests.SessionStub import SessionStub
from src.processing.CameraProcessor import CameraProcessor
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.CameraDataHandler import CameraDataHandler
from tests.collection.stubs.CameraCollectorStub import CameraCollectorStub


class CameraTest(unittest.TestCase):
    def test(self):
        # collecting
        camera_collector = CameraCollectorStub()
        camera_collector.start()
        camera_collector.join()
        data = camera_collector.stop_collect()

        # processing
        self.cpt = CameraProcessor()
        session_duration = 5
        st = time.time()
        session = SessionStub("CameraProcessingDBTest", session_duration, st)
        self.cpt.set_arguements(data, session)
        self.cpt.start()
        self.cpt.join()
        print(time.time() - st)

        # database
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')

        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        st = time.time()
        data_handler = CameraDataHandler(path=self.out_path)
        data_handler.save((session.session_name, self.cpt.features))
        print(time.time() - st)
        res = manager.ask(f"SELECT * FROM Camera WHERE session='{session.session_name}'")
        self.assertTrue(len(res) == 1)
        key = res[0][0]
        data = res[0][1]
        self.assertEqual(key, session.session_name)
        data = msgpack.unpackb(data, object_hook=m.decode)
        self.assertTrue(np.array_equal(data, np.array(self.cpt.features)))


if __name__ == '__main__':
    unittest.main()
