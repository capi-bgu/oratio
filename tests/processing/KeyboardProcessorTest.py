import time
import logging
import unittest
from threading import Thread
from tests.SessionStub import SessionStub
from oratio.processing.KeyboardProcessor import KeyboardProcessor
from tests.collection.stubs.KeyboardCollectorStub import KeyboardCollectorStub
from tests.database.sqlite_db.stubs.KeyboardDataHandlerStub import KeyboardDataHandlerStub


class KeyboardProcessorTest(unittest.TestCase):
    def test(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        keyboard_collector = KeyboardCollectorStub()
        keyboard_collector.start_collect()
        start_time, data = keyboard_collector.stop_collect()

        self.keyboard_processor = KeyboardProcessor()
        session_duration = 5
        session = SessionStub("KeyboardProcessingTest", session_duration, start_time)
        processor = Thread(target=self.keyboard_processor.process_data, args=(data, session))
        st = time.time()
        processor.start()
        processor.join()
        features = self.keyboard_processor.features
        logging.debug(time.time() - st)

        self.assertAlmostEqual(features['typing_speed'], 3.8, delta=0.5)
        self.assertAlmostEqual(features['active_typing_speed'], 7.38, delta=0.5)
        self.assertAlmostEqual(features['average_press_duration'], 0.04, delta=0.5)
        self.assertAlmostEqual(features['average_down_to_down'], 0.08, delta=0.5)
        self.assertEqual(features['regular_press_count'], 16)
        self.assertEqual(features['punctuations_press_count'], 0)
        self.assertEqual(features['space_counter'], 3)
        self.assertEqual(features['error_corrections'], 0)
        self.assertEqual(features['mode_key'], ord('e'.upper()))
        self.assertAlmostEqual(features['idle_time'], 2.5, delta=0.5)
        self.assertEqual(features['unique_events'], 10)

        data_handler = KeyboardDataHandlerStub(name="processed")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()
