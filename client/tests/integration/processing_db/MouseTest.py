import os
import time
import pathlib
import unittest

from src.database.sqlite_db.MouseDataHandler import MouseDataHandler
from src.processing.MouseProcessor import MouseProcessor
from tests.SessionStub import SessionStub
from src.database.sqlite_db.SqliteManager import SqliteManager
from tests.collection.stubs.MouseCollectorStub import MouseCollectorStub


class KeyboardTest(unittest.TestCase):
    def test(self):
        mouse_collector = MouseCollectorStub()
        mouse_collector.start()
        mouse_collector.join()
        start_time, data = mouse_collector.stop_collect()

        self.mpt = MouseProcessor()
        session_duration = 5
        session = SessionStub(0, session_duration, start_time)
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
        data_handler.save(("MouseIntegrationTest", self.mpt.features))
        print(time.time() - st)


if __name__ == '__main__':
    unittest.main()
