import time
import logging
import unittest
from pynput import keyboard
from threading import Thread
from tests.SessionStub import SessionStub
from pynput.keyboard import Controller as KeyboardController
from oratio.collection.PynputKeyboardCollector import PynputKeyboardCollector
from oratio.processing.PynputKeyboardProcessor import PynputKeyboardProcessor
from tests.database.sqlite_db.stubs.KeyboardDataHandlerStub import KeyboardDataHandlerStub


class KeyboardTest(unittest.TestCase):
    def test(self):
        self.keyboard_controller = KeyboardController()
        self.keyboard_collector = PynputKeyboardCollector()
        self.keyboard_processor = PynputKeyboardProcessor()
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        self.st = time.time()
        session = SessionStub("KeyboardCollectingProcessingTest", 5, self.st)

        # collecting
        st = time.time()
        text = "hello from the test"
        user = Thread(target=self.simulate_user, args=(text,))
        collector = Thread(target=self.keyboard_collector.start_collect)
        collector.start()
        user.start()
        time.sleep(session.duration)
        data = self.keyboard_collector.stop_collect()
        collector.join()
        logging.debug(time.time() - st)
        user.join()

        # processing
        st = time.time()
        processor = Thread(target=self.keyboard_processor.process_data, args=(data, session))
        processor.start()
        processor.join()
        features = self.keyboard_processor.features
        logging.debug(time.time() - st)
        print(features)
        self.assertAlmostEqual(features['typing_speed'], 3.8, delta=0.5)
        self.assertAlmostEqual(features['active_typing_speed'], 7.3, delta=0.5)
        self.assertAlmostEqual(features['average_press_duration'], 0.04, delta=0.5)
        self.assertAlmostEqual(features['average_down_to_down'], 0.08, delta=0.5)
        self.assertEqual(features['regular_press_count'], 16)
        self.assertEqual(features['punctuations_press_count'], 0)
        self.assertEqual(features['space_counter'], 3)
        self.assertEqual(features['error_corrections'], 0)
        self.assertEqual(features['mode_key'], ord('e'.upper()))
        self.assertAlmostEqual(features['idle_time'], 2.5, delta=0.5)
        self.assertEqual(features['unique_events'], 10)

        # database
        data_handler = KeyboardDataHandlerStub(name="gathered")
        data_handler.save(features)

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