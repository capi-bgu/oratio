import os
import time
import logging
import pathlib
import unittest
from threading import Thread
from pynput.mouse import Button
from tests.SessionStub import SessionStub
from pynput.mouse import Controller as MouseController
from oratio.processing.MouseProcessor import MouseProcessor
from oratio.collection.MouseCollector import MouseCollector
from tests.database.sqlite_db.stubs.MouseDataHandlerStub import MouseDataHandlerStub


class MouseTest(unittest.TestCase):
    def test(self):
        self.mouse_controller = MouseController()
        self.mouse_processor = MouseProcessor()
        self.mouse_collector = MouseCollector()
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        self.st = time.time()
        session = SessionStub("PynputMouseCollectingProcessingTest", 5, self.st)

        # collecting
        st = time.time()
        user = Thread(target=self.simulate_user)
        collector = Thread(target=self.mouse_collector.start_collect)
        collector.start()
        user.start()
        time.sleep(session.duration)
        data = self.mouse_collector.stop_collect()
        collector.join()
        logging.debug(time.time() - st)
        user.join()

        # processing
        st = time.time()
        processor = Thread(target=self.mouse_processor.process_data, args=(data, session))
        processor.start()
        processor.join()
        logging.debug(time.time() - st)
        features = self.mouse_processor.features
        self.assertEqual(features['right_click_count'], 1)
        self.assertEqual(features['left_click_count'], 4)
        # self.assertAlmostEqual(features['scroll_speed'],  ????, delta=0.5)
        self.assertEqual(features['double_click_count'], 2)
        self.assertAlmostEqual(features['cursor_x_distance'], 0, delta=0.5)
        self.assertAlmostEqual(features['cursor_y_distance'], 0, delta=0.5)
        self.assertAlmostEqual(features['average_momentary_speed_x'], 0, delta=0.5)
        self.assertAlmostEqual(features['average_momentary_speed_y'], 0, delta=0.5)
        self.assertAlmostEqual(features['average_speed_x'], 0, delta=0.5)
        self.assertAlmostEqual(features['average_speed_y'], 0, delta=0.5)
        self.assertAlmostEqual(features['average_active_speed_x'], 0, delta=0.5)
        self.assertAlmostEqual(features['average_active_speed_y'], 0, delta=0.5)
        self.assertAlmostEqual(features['average_cursor_angle'], 0, delta=0.5)
        self.assertAlmostEqual(features['std_cursor_angle'], 0, delta=0.5)
        self.assertAlmostEqual(features['Turn_0_45'], 0, delta=0.5)
        self.assertAlmostEqual(features['Turn_45_90'], 0, delta=0.5)
        self.assertAlmostEqual(features['Turn_90_135'], 0, delta=0.5)
        self.assertAlmostEqual(features['Turn_135_180'], 0, delta=0.5)
        self.assertAlmostEqual(features['Direction_S'], 0, delta=0.5)
        self.assertAlmostEqual(features['Direction_SW'], 0, delta=0.5)
        self.assertAlmostEqual(features['Direction_W'], 0, delta=0.5)
        self.assertAlmostEqual(features['Direction_NW'], 0, delta=0.5)
        self.assertAlmostEqual(features['Direction_N'], 0, delta=0.5)
        self.assertAlmostEqual(features['Direction_NE'], 0, delta=0.5)
        self.assertAlmostEqual(features['Direction_E'], 0, delta=0.5)
        self.assertAlmostEqual(features['Direction_SE'], 0, delta=0.5)
        self.assertAlmostEqual(features['Dist1'], 0, delta=0.5)
        self.assertAlmostEqual(features['Dist2'], 0, delta=0.5)
        self.assertAlmostEqual(features['Dist3'], 0, delta=0.5)
        self.assertAlmostEqual(features['idle_time'], 3.9, delta=0.5)
        self.assertAlmostEqual(features['right_click_duration'], 0.05, delta=0.5)
        self.assertAlmostEqual(features['left_click_duration'], 0.0125, delta=0.5)

        # database
        data_handler = MouseDataHandlerStub(name="gathered")
        data_handler.save(features)

    def save_data(self, data):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        output_path = os.path.join(test_dir, 'test_output', 'mouse')

        f = open(f"{output_path}\\_mouse.txt", "w+")
        f.write(str(self.st) + '\n')
        for i, e in enumerate(data):
            f.write(str(i) + '. ' + str(e.__dict__) + '\n')
        f.close()

    def simulate_user(self):
        time.sleep(1.5)
        self.mouse_controller.press(Button.right)
        time.sleep(0.05)
        self.mouse_controller.release(Button.right)
        time.sleep(0.3)
        self.mouse_controller.move(-20, 20)
        time.sleep(0.01)
        self.mouse_controller.press(Button.left)
        time.sleep(0.05)
        self.mouse_controller.release(Button.left)
        time.sleep(0.7)
        self.mouse_controller.click(Button.left, 3)
        time.sleep(0.3)
        self.mouse_controller.scroll(0, 5)
        time.sleep(0.3)
        self.mouse_controller.scroll(0, -5)


if __name__ == '__main__':
    unittest.main()
