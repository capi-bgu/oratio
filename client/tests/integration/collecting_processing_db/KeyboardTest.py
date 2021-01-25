import os
import time
import pathlib
import unittest

from tests.SessionStub import SessionStub
from src.processing.KeyboardProcessor import KeyboardProcessor
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.collection.KeyboardCollector import KeyboardCollector
from src.database.sqlite_db.KeyboardDataHandler import KeyboardDataHandler


class KeyboardTest(unittest.TestCase):
    def test(self):
        st = time.time()
        session = SessionStub("KeyboardFullTest", 5, st)

        keyboard_collector = KeyboardCollector()
        keyboard_collector.start()
        time.sleep(session.session_duration)
        data = keyboard_collector.stop_collect()
        keyboard_collector.join()
        print(time.time() - st)

        self.kbpt = KeyboardProcessor()
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
        data_handler.save((session.session_name, self.kbpt.features))
        print(time.time() - st)


if __name__ == '__main__':
    unittest.main()
