import time
import unittest
from tests.SessionStub import SessionStub
from src.processing.MouseProcessor import MouseProcessor
from tests.collection.stubs.MouseCollectorStub import MouseCollectorStub
from tests.database.sqlite_db.stubs.MouseDataHandlerStub import MouseDataHandlerStub


class MouseProcessorTest(unittest.TestCase):
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
        features = self.mpt.features
        print(time.time() - st)

        self.assertEqual(features['right_click_count'],  1)
        self.assertEqual(features['left_click_count'],  4)
        # self.assertAlmostEqual(features['scroll_speed'],  ????, delta=0.05)
        self.assertEqual(features['double_click_count'],  2)
        self.assertAlmostEqual(features['cursor_x_distance'],  0, delta=0.05)
        self.assertAlmostEqual(features['cursor_y_distance'],  0, delta=0.05)
        self.assertAlmostEqual(features['average_momentary_speed_x'],  0, delta=0.05)
        self.assertAlmostEqual(features['average_momentary_speed_y'],  0, delta=0.05)
        self.assertAlmostEqual(features['average_speed_x'],  0, delta=0.05)
        self.assertAlmostEqual(features['average_speed_y'],  0, delta=0.05)
        self.assertAlmostEqual(features['average_active_speed_x'],  0, delta=0.05)
        self.assertAlmostEqual(features['average_active_speed_y'],  0, delta=0.05)
        self.assertAlmostEqual(features['average_cursor_x_angle'],  0, delta=0.05)
        self.assertAlmostEqual(features['average_cursor_y_angle'],  0, delta=0.05)
        self.assertAlmostEqual(features['cursor_distance_ratio'],  0, delta=0.05)
        self.assertAlmostEqual(features['idle_time'],  3.9, delta=0.05)
        self.assertAlmostEqual(features['right_click_duration'],  0.05, delta=0.05)
        self.assertAlmostEqual(features['left_click_duration'],  0.0125, delta=0.06)

        data_handler = MouseDataHandlerStub(name="processed")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()
