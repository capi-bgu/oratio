import os
import time
import pathlib
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
        camera_collector = CameraCollector(fps=2)
        camera_collector.start()
        time.sleep(session.session_duration)
        data = camera_collector.stop_collect()
        camera_collector.join()
        print(time.time() - st)
        self.assertEqual(len(data), session.session_duration * camera_collector.fps)

        # processing
        self.cpt = CameraProcessor()
        self.cpt.set_arguements(data, session)
        st = time.time()
        self.cpt.start()
        self.cpt.join()
        print(time.time() - st)
        features = self.cpt.features
        self.assertLessEqual(len(features), session.session_duration * camera_collector.fps)
        for img in features:
            self.assertTupleEqual(img.shape, (150, 150))

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
