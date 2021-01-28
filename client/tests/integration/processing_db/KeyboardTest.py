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

        # collecting
        keyboard_collector = KeyboardCollectorStub()
        keyboard_collector.start()
        keyboard_collector.join()
        start_time, data = keyboard_collector.stop_collect()

        # processing
        self.kbpt = KeyboardProcessor()
        session_duration = 5
        session = SessionStub('KeyboardIntegrationTest', session_duration, start_time)
        self.kbpt.set_arguements(data, session)
        st = time.time()
        self.kbpt.start()
        self.kbpt.join()
        print(time.time() - st)

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')

        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        st = time.time()
        data_handler = KeyboardDataHandler(path=self.out_path)
        data_handler.save((session.session_name, self.kbpt.features))
        print(time.time() - st)
        res = manager.ask(f"SELECT * FROM Keyboard WHERE session='{session.session_name}'")
        self.assertTrue(len(res) == 1)
        key = res[0][0]
        self.assertEqual(key, session.session_name)
        for i, val in enumerate(list(self.kbpt.features.values())):
            self.assertEqual(val, res[0][i + 1])


if __name__ == '__main__':
    unittest.main()
