import os
import pickle
import pathlib
import unittest
import numpy as np
from threading import Thread
from oratio.database.sqlite_db.SqliteManager import SqliteManager
from oratio.database.sqlite_db.CameraDataHandler import CameraDataHandler
from tests.processing.stubs.CameraProcessorStub import CameraProcessorStub


class CameraDataHandlerTest(unittest.TestCase):

    def test(self):
        session_name = "CameraHandlerTest"

        camera_processor = CameraProcessorStub()
        processor = Thread(target=camera_processor.process_data, args=(None, None))
        processor.start()
        processor.join()

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        manager = SqliteManager(path=self.out_path)
        manager.create_data_holder()

        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='Camera';")
        self.assertNotIn(("Camera",), res)

        self.data_handler = CameraDataHandler(path=self.out_path)
        self.data_handler.create_data_holder()
        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='Camera';")
        self.assertIn(("Camera",), res)

        res = manager.ask(f"SELECT * FROM Camera WHERE session='{session_name}'")
        self.assertEqual(len(res), 0)

        self.data_handler.save(('CameraHandlerTest', camera_processor.features))
        res = manager.ask(f"SELECT * FROM Camera WHERE session='{session_name}'")
        self.assertEqual(len(res), 1)
        key = res[0][0]
        data = res[0][1]
        data = pickle.loads(data)
        self.assertEqual(key, session_name)
        self.assertEqual(len(data), len(camera_processor.features))
        for ret, expected in zip(data, camera_processor.features):
            self.assertTrue(np.array_equal(ret, expected))


if __name__ == '__main__':
    unittest.main()
