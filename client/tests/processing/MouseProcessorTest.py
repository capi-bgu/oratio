import time
import unittest
from threading import Thread

from tests.SessionStub import SessionStub
from src.processing.MouseProcessor import MouseProcessor
from tests.collection.stubs.MouseCollectorStub import MouseCollectorStub
from tests.database.sqlite_db.stubs.MouseDataHandlerStub import MouseDataHandlerStub


class MouseProcessorTest(unittest.TestCase):
    def test(self):
        mouse_collector = MouseCollectorStub()
        mouse_collector.start_collect()
        start_time, data = mouse_collector.stop_collect()

        self.mouse_processor = MouseProcessor()
        session_duration = 5
        session = SessionStub(0, session_duration, start_time)
        processor = Thread(target=self.mouse_processor.process_data, args=(data, session))
        st = time.time()
        processor.start()
        processor.join()
        features = self.mouse_processor.features
        print(time.time() - st)

        self.assertEqual(features['right_click_count'], 1)
        self.assertEqual(features['left_click_count'], 4)
        # self.assertAlmostEqual(features['scroll_speed'],  ????, delta=0.1)
        self.assertEqual(features['double_click_count'], 2)
        self.assertAlmostEqual(features['cursor_x_distance'], 0, delta=0.1)
        self.assertAlmostEqual(features['cursor_y_distance'], 0, delta=0.1)
        self.assertAlmostEqual(features['average_momentary_speed_x'], 0, delta=0.1)
        self.assertAlmostEqual(features['average_momentary_speed_y'], 0, delta=0.1)
        self.assertAlmostEqual(features['average_speed_x'], 0, delta=0.1)
        self.assertAlmostEqual(features['average_speed_y'], 0, delta=0.1)
        self.assertAlmostEqual(features['average_active_speed_x'], 0, delta=0.1)
        self.assertAlmostEqual(features['average_active_speed_y'], 0, delta=0.1)
        self.assertAlmostEqual(features['average_cursor_angle'], 0, delta=0.1)
        self.assertAlmostEqual(features['std_cursor_angle'], 0, delta=0.1)
        self.assertAlmostEqual(features['Turn_0_45'], 0, delta=0.1)
        self.assertAlmostEqual(features['Turn_45_90'], 0, delta=0.1)
        self.assertAlmostEqual(features['Turn_90_135'], 0, delta=0.1)
        self.assertAlmostEqual(features['Turn_135_180'], 0, delta=0.1)
        self.assertAlmostEqual(features['Direction_S'], 0, delta=0.1)
        self.assertAlmostEqual(features['Direction_SW'], 0, delta=0.1)
        self.assertAlmostEqual(features['Direction_W'], 0, delta=0.1)
        self.assertAlmostEqual(features['Direction_NW'], 0, delta=0.1)
        self.assertAlmostEqual(features['Direction_N'], 0, delta=0.1)
        self.assertAlmostEqual(features['Direction_NE'], 0, delta=0.1)
        self.assertAlmostEqual(features['Direction_E'], 0, delta=0.1)
        self.assertAlmostEqual(features['Direction_SE'], 0, delta=0.1)
        self.assertAlmostEqual(features['Dist1'], 0, delta=0.1)
        self.assertAlmostEqual(features['Dist2'], 0, delta=0.1)
        self.assertAlmostEqual(features['Dist3'], 0, delta=0.1)
        self.assertAlmostEqual(features['idle_time'], 3.9, delta=0.1)
        self.assertAlmostEqual(features['right_click_duration'], 0.05, delta=0.1)
        self.assertAlmostEqual(features['left_click_duration'], 0.0125, delta=0.1)

        data_handler = MouseDataHandlerStub(name="processed")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()
