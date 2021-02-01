import os
import time
import pathlib
import unittest
from threading import Thread
from tests.SessionStub import SessionStub
from src.processing.KeyboardProcessor import KeyboardProcessor
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.KeyboardDataHandler import KeyboardDataHandler
from tests.collection.stubs.KeyboardCollectorStub import KeyboardCollectorStub


class KeyboardTest(unittest.TestCase):
    def test(self):
        # collecting
        keyboard_collector = KeyboardCollectorStub()
        keyboard_collector.start_collect()
        start_time, data = keyboard_collector.stop_collect()

        # processing
        self.keyboard_processor = KeyboardProcessor()
        session_duration = 5
        session = SessionStub('KeyboardIntegrationTest', session_duration, start_time)
        processor = Thread(target=self.keyboard_processor.process_data, args=(data, session))
        st = time.time()
        processor.start()
        processor.join()
        print(time.time() - st)

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')

        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        st = time.time()
        data_handler = KeyboardDataHandler(path=self.out_path)
        data_handler.create_data_holder()
        data_handler.save((session.id, self.keyboard_processor.features))
        print(time.time() - st)
        res = manager.ask(f"SELECT * FROM Keyboard WHERE session='{session.id}'")
        self.assertEqual(len(res), 1)
        key = res[0][0]
        self.assertEqual(key, session.id)
        for i, val in enumerate(list(self.keyboard_processor.features.values())):
            self.assertEqual(val, res[0][i + 1])


if __name__ == '__main__':
    unittest.main()
