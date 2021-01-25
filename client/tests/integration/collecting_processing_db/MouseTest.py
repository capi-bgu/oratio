import os
import time
import pathlib
import unittest
from tests.SessionStub import SessionStub
from src.collection.MouseCollector import MouseCollector
from src.processing.MouseProcessor import MouseProcessor
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.MouseDataHandler import MouseDataHandler


class KeyboardTest(unittest.TestCase):
    def test(self):
        st = time.time()
        session = SessionStub("MouseFullTest", 5, st)

        mouse_collector = MouseCollector()
        mouse_collector.start()
        time.sleep(session.session_duration)
        data = mouse_collector.stop_collect()
        mouse_collector.join()
        print(time.time() - st)

        self.mpt = MouseProcessor()
        self.mpt.set_arguements(data, session)
        st = time.time()
        self.mpt.start()
        self.mpt.join()
        print(time.time() - st)

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        st = time.time()
        data_handler = MouseDataHandler(path=self.out_path)
        data_handler.save((session.session_name, self.mpt.features))
        print(time.time() - st)


if __name__ == '__main__':
    unittest.main()
