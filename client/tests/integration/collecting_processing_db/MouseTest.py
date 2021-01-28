import os
import time
import pathlib
import unittest
from threading import Thread
from pynput.mouse import Button
from tests.SessionStub import SessionStub
from pynput.mouse import Controller as MouseController
from src.collection.MouseCollector import MouseCollector
from src.processing.MouseProcessor import MouseProcessor
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.MouseDataHandler import MouseDataHandler


class MouseTest(unittest.TestCase):
    def test(self):
        st = time.time()
        session = SessionStub("MouseFullTest", 5, st)
        self.mouse_controller = MouseController()


        # collecting
        mouse_collector = MouseCollector()
        mouse_collector.start()
        user = Thread(target=self.simulate_user)
        user.start()
        time.sleep(session.session_duration)
        data = mouse_collector.stop_collect()
        mouse_collector.join()
        print(time.time() - st)
        user.join()

        # processing
        self.mpt = MouseProcessor()
        self.mpt.set_arguements(data, session)
        st = time.time()
        self.mpt.start()
        self.mpt.join()
        print(time.time() - st)
        features = self.mpt.features
        self.assertEqual(features['right_click_count'], 1)
        self.assertEqual(features['left_click_count'], 4)
        # self.assertAlmostEqual(features['scroll_speed'],  ????, delta=0.05)
        self.assertEqual(features['double_click_count'], 2)
        self.assertAlmostEqual(features['cursor_x_distance'], 0, delta=0.05)
        self.assertAlmostEqual(features['cursor_y_distance'], 0, delta=0.05)
        self.assertAlmostEqual(features['average_momentary_speed_x'], 0, delta=0.05)
        self.assertAlmostEqual(features['average_momentary_speed_y'], 0, delta=0.05)
        self.assertAlmostEqual(features['average_speed_x'], 0, delta=0.05)
        self.assertAlmostEqual(features['average_speed_y'], 0, delta=0.05)
        self.assertAlmostEqual(features['average_active_speed_x'], 0, delta=0.05)
        self.assertAlmostEqual(features['average_active_speed_y'], 0, delta=0.05)
        self.assertAlmostEqual(features['average_cursor_x_angle'], 0, delta=0.05)
        self.assertAlmostEqual(features['average_cursor_y_angle'], 0, delta=0.05)
        self.assertAlmostEqual(features['cursor_distance_ratio'], 0, delta=0.05)
        self.assertAlmostEqual(features['idle_time'], 3.9, delta=0.05)
        self.assertAlmostEqual(features['right_click_duration'], 0.05, delta=0.05)
        self.assertAlmostEqual(features['left_click_duration'], 0.0125, delta=0.06)

        # database
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')

        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        st = time.time()
        data_handler = MouseDataHandler(path=self.out_path)
        data_handler.save((session.session_name, self.mpt.features))
        print(time.time() - st)
        res = manager.ask(f"SELECT * FROM Mouse WHERE session='{session.session_name}'")
        self.assertTrue(len(res) == 1)
        key = res[0][0]
        self.assertEqual(key, session.session_name)
        for i, val in enumerate(list(self.mpt.features.values())):
            self.assertEqual(val, res[0][i + 1])

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
