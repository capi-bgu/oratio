import os
import pathlib
import time
import unittest

from src.database.sqlite_db.CameraDataHandler import CameraDataHandler
from src.database.sqlite_db.SqliteManager import SqliteManager
from tests.SessionStub import SessionStub
from src.processing.CameraProcessor import CameraProcessor
from tests.collection.stubs.CameraCollectorStub import CameraCollectorStub
from tests.database.sqlite_db.stubs.CameraDataHandlerStub import CameraDataHandlerStub
from tests.processing.stubs.CameraProcessorStub import CameraProcessorStub


class CameraDataHandlerTest(unittest.TestCase):
    def test(self):
        camera_processor = CameraProcessorStub()
        camera_processor.start()
        camera_processor.join()

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/img"):
            os.mkdir("../test_output/img")
        self.out_path = os.path.join(test_dir, 'test_output', 'img')

        manager = SqliteManager(path=self.out_path)
        manager.create_database()
        data_handler = CameraDataHandler(path=self.out_path)
        data_handler.save(("CameraHandlerTest", camera_processor.features))


if __name__ == '__main__':
    unittest.main()
