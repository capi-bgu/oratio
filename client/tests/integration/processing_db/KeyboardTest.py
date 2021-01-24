import os
import time
import pathlib
import unittest
from tests.SessionStub import SessionStub
from src.processing.KeyboardProcessor import KeyboardProcessor
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.KeyboardDataHandler import KeyboardDataHandler
from tests.collection.stubs.KeyboardCollectorStub import KeyboardCollectorStub


class KeyboardTest(unittest.TestCase):
    def test(self):
        keyboard_collector = KeyboardCollectorStub()
        keyboard_collector.start()
        keyboard_collector.join()
        start_time, data = keyboard_collector.stop_collect()

        self.kbpt = KeyboardProcessor()
        session_duration = 5
        session = SessionStub(0, session_duration, start_time)
        self.kbpt.set_arguements(data, session)

        st = time.time()
        self.kbpt.start()
        self.kbpt.join()
        print(time.time() - st)

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        st = time.time()
        data_handler = KeyboardDataHandler(path=self.out_path)
        data_handler.save(("KeyboardIntegrationTest", self.kbpt.features))
        print(time.time() - st)


if __name__ == '__main__':
    unittest.main()
