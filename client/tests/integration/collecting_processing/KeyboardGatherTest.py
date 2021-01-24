import time
import unittest
from tests.SessionStub import SessionStub
from src.collection.KeyboardCollector import KeyboardCollector
from src.processing.KeyboardProcessor import KeyboardProcessor
from tests.database.sqlite_db.stubs.KeyboardDataHandlerStub import KeyboardDataHandlerStub


class KeyboardGatherTest(unittest.TestCase):
    def test(self):
        keyboard_processor = KeyboardProcessor()
        keyboard_collector = KeyboardCollector()

        self.st = time.time()
        session = SessionStub(1, 5, self.st)

        st = time.time()
        keyboard_collector.start()
        time.sleep(session.session_duration)
        data = keyboard_collector.stop_collect()
        keyboard_collector.join()
        print(time.time() - st)

        st = time.time()
        keyboard_processor.set_arguements(data, session)
        keyboard_processor.start()
        keyboard_processor.join()
        features = keyboard_processor.features
        print(time.time() - st)

        data_handler = KeyboardDataHandlerStub(name="gathered")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()
