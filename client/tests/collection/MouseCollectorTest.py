import os
import time
import pathlib
import unittest
from threading import Thread
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from src.collection.MouseCollector import MouseCollector


class MouseCollectorTest(unittest.TestCase):
    def test(self):
        self.mouse_controller = MouseController()
        self.mouse_collector = MouseCollector()
        self.session_duration = 5
        self.start_time = time.time()
        collector = Thread(target=self.mouse_collector.start_collect)
        collector.start()
        user = Thread(target=self.simulate_user)
        user.start()
        time.sleep(self.session_duration)
        data = self.mouse_collector.stop_collect()
        collector.join()
        user.join()

        self.assertEqual(data[0].MessageName, "mouse right down")
        self.assertEqual(data[1].MessageName, "mouse right up")

        self.assertEqual(data[2].MessageName, "mouse left down")
        self.assertEqual(data[3].MessageName, "mouse left up")

        self.assertEqual(data[4].MessageName, "mouse left down")
        self.assertEqual(data[5].MessageName, "mouse left up")

        self.assertEqual(data[6].MessageName, "mouse left down")
        self.assertEqual(data[7].MessageName, "mouse left up")

        self.assertEqual(data[8].MessageName, "mouse left down")
        self.assertEqual(data[9].MessageName, "mouse left up")

        self.assertEqual(data[10].MessageName, "mouse wheel")
        self.assertEqual(data[11].MessageName, "mouse wheel")

        self.process_data(data)

    def process_data(self, data):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        output_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        output_path = os.path.join(output_path, 'mouse')
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        f = open(f"{output_path}\\raw_mouse.txt", "w+")
        f.write(str(self.start_time) + '\n')
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
