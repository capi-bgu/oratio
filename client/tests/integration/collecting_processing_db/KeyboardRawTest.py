import os
import time
import pickle
import pathlib
import unittest
from pynput import keyboard
from threading import Thread
from tests.SessionStub import SessionStub
from pynput.keyboard import Controller as KeyboardController
from src.processing.IdentityProcessor import IdentityProcessor
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.collection.KeyboardCollector import KeyboardCollector
from src.database.sqlite_db.RawDataHandler import RawDataHandler


class KeyboardRawTest(unittest.TestCase):
    def test(self):
        st = time.time()
        session = SessionStub("KeyboardFullRawTest", 5, st)
        self.keyboard_controller = KeyboardController()
        self.keyboard_collector = KeyboardCollector()

        # collecting
        text = "hello from the test"
        collector = Thread(target=self.keyboard_collector.start_collect)
        user = Thread(target=self.simulate_user, args=(text,))
        st = time.time()
        collector.start()
        user.start()
        time.sleep(session.duration)
        data = self.keyboard_collector.stop_collect()
        collector.join()
        print(time.time() - st)
        user.join()

        # processing
        self.keyboard_processor = IdentityProcessor()
        processor = Thread(target=self.keyboard_processor.process_data, args=(data, session))
        processor.start()
        processor.join()
        print(time.time() - st)

        # database
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')

        manager = SqliteManager(path=self.out_path)
        manager.create_data_holder()

        st = time.time()
        data_handler = RawDataHandler(name="KeyboardRawData", path=self.out_path)
        data_handler.create_data_holder()
        data_handler.save((session.id, self.keyboard_processor.features))
        print(time.time() - st)
        res = manager.ask(f"SELECT * FROM KeyboardRawData WHERE session='{session.id}'")
        self.assertEqual(len(res), 1)
        key = res[0][0]
        data = res[0][1]
        data = pickle.loads(data)
        self.assertEqual(key, session.id)
        self.assertEqual(len(data), len(self.keyboard_processor.features))
        for ret, expected in zip(data, self.keyboard_processor.features):
            self.assertEqual(ret.__dict__, expected.__dict__)

    def simulate_user(self, text):
        time.sleep(1.5)
        for c in text:
            key_press_duration = 0.04
            self.simulate_press(c, key_press_duration)
            key_down_to_down = 0.08
            time.sleep(key_down_to_down)

    def simulate_press(self, character, key_press_duration):
        key = keyboard.KeyCode(char=character)
        self.keyboard_controller.press(key)
        time.sleep(key_press_duration)
        self.keyboard_controller.release(key)


if __name__ == '__main__':
    unittest.main()
