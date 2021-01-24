import os
import pathlib
import unittest
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
        data_handler = CameraDataHandler(path=self.out_path)
        data_handler.save(("CameraHandlerTest", camera_processor.features))


if __name__ == '__main__':
    unittest.main()
