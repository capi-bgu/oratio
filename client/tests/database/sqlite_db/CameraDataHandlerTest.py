import os
import pathlib
import unittest
import msgpack
import msgpack_numpy as m
import numpy as np

from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.CameraDataHandler import CameraDataHandler
from tests.processing.stubs.CameraProcessorStub import CameraProcessorStub


class CameraDataHandlerTest(unittest.TestCase):

    def test(self):
        camera_processor = CameraProcessorStub()
        camera_processor.set_arguements(None, None)
        camera_processor.start()
        camera_processor.join()

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)


        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='Camera';")
        self.assertNotIn("Camera", res)

        self.data_handler = CameraDataHandler(path=self.out_path)
        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='Camera';")
        self.assertIn(("Camera",), res)

        res = manager.ask(f"SELECT * FROM Camera WHERE session='CameraHandlerTest'")
        self.assertTrue(len(res) == 0)

        self.data_handler.save(('CameraHandlerTest', camera_processor.features))
        res = manager.ask(f"SELECT * FROM Camera WHERE session='CameraHandlerTest'")
        self.assertTrue(len(res) == 1)
        key = res[0][0]
        data = res[0][1]
        self.assertEqual(key, 'CameraHandlerTest')
        data = msgpack.unpackb(data, object_hook=m.decode)
        self.assertTrue(np.array_equal(data, np.array(camera_processor.features)))


if __name__ == '__main__':
    unittest.main()
