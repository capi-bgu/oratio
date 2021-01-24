import json
import os
import time
import pathlib
import unittest
from tests.SessionStub import SessionStub
from src.processing.KeyboardProcessor import KeyboardProcessor
from tests.collection.stubs.KeyboardCollectorStub import KeyboardCollectorStub
from tests.database.sqlite_db.stubs.KeyboardDataHandlerStub import KeyboardDataHandlerStub


class KeyboardProcessorTest(unittest.TestCase):
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
        features = self.kbpt.features
        print(time.time() - st)

        data_handler = KeyboardDataHandlerStub(name="processed")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()
