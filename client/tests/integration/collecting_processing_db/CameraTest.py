import os
import time
import pathlib
import unittest
from tests.SessionStub import SessionStub
from src.collection.CameraCollector import CameraCollector
from src.processing.CameraProcessor import CameraProcessor
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.CameraDataHandler import CameraDataHandler


class CameraTest(unittest.TestCase):
    def test(self):
        st = time.time()
        session = SessionStub("CameraFullTest", 5, st)

        camera_collector = CameraCollector(fps=2)
        camera_collector.start()
        time.sleep(session.session_duration)
        data = camera_collector.stop_collect()
        camera_collector.join()
        print(time.time() - st)

        self.cpt = CameraProcessor()
        self.cpt.set_arguements(data, session)
        st = time.time()
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
        data_handler.save((session.session_name, self.cpt.features))
        print(time.time() - st)


if __name__ == '__main__':
    unittest.main()
