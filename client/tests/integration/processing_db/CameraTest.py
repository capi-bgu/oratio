import os
import time
import pathlib
import unittest
from tests.SessionStub import SessionStub
from src.processing.CameraProcessor import CameraProcessor
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.CameraDataHandler import CameraDataHandler
from tests.collection.stubs.CameraCollectorStub import CameraCollectorStub


class CameraTest(unittest.TestCase):
    def test(self):
        camera_collector = CameraCollectorStub()
        camera_collector.start()
        camera_collector.join()
        data = camera_collector.stop_collect()

        self.cpt = CameraProcessor()
        session_duration = 5
        st = time.time()
        session = SessionStub(0, session_duration, st)
        self.cpt.set_arguements(data, session)
        self.cpt.start()
        self.cpt.join()
        print(time.time() - st)

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        st = time.time()
        data_handler = CameraDataHandler(path=self.out_path)
        data_handler.save(("CameraIntegrationTest", self.cpt.features))
        print(time.time() - st)


if __name__ == '__main__':
    unittest.main()
