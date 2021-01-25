import os
import time
import pathlib
import unittest
from threading import Thread
from src.collection.MouseCollector import MouseCollector
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button


class MouseCollectorTest(unittest.TestCase):
    def test(self):
        self.mouse_controller = MouseController()
        self.mouse_collector = MouseCollector()
        self.session_duration = 5
        self.mouse_collector.start()
        Thread(target=self.simulate_user).start()
        time.sleep(self.session_duration)
        data = self.mouse_collector.stop_collect()
        self.mouse_collector.join()

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
        for i, e in enumerate(data):
            f.write(str(i) + '. ' + str(e.__dict__) + '\n')
        f.close()

    def simulate_user(self):
        time.sleep(0.5)
        self.mouse_controller.move(5, -5)
        time.sleep(0.3)
        self.mouse_controller.click(Button.left, 1)
        time.sleep(0.3)
        self.mouse_controller.click(Button.right, 1)
        time.sleep(0.3)
        self.mouse_controller.click(Button.middle, 1)
        time.sleep(0.3)
        self.mouse_controller.move(-5, 5)
        time.sleep(0.3)
        self.mouse_controller.click(Button.left, 2)
        time.sleep(0.3)
        self.mouse_controller.click(Button.right, 2)
        time.sleep(0.3)

        self.mouse_controller.press(Button.left)
        time.sleep(0.3)
        self.mouse_controller.release(Button.left)
        time.sleep(0.3)

        self.mouse_controller.scroll(0, 2)
        time.sleep(0.3)
        self.mouse_controller.scroll(0, -2)


if __name__ == '__main__':
    unittest.main()
