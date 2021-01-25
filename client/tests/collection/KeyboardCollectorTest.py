import os
import time
import random
import pathlib
import unittest
from pynput import keyboard
from threading import Thread
from src.collection.KeyboardCollector import KeyboardCollector
from pynput.keyboard import Controller as KeyboardController


class KeyboardCollectorTest(unittest.TestCase):
    def test(self):
        self.keyboard_controller = KeyboardController()
        self.keyboard_collector = KeyboardCollector()
        self.session_duration = 5
        self.keyboard_collector.start()

        text = "hello from keyboard collector test"
        Thread(target=self.simulate_user, args=(text,)).start()

        time.sleep(self.session_duration)
        data = self.keyboard_collector.stop_collect()
        self.keyboard_collector.join()

        for i, c in enumerate(text):
            i *= 2
            self.assertEqual(chr(data[i].Ascii), c)
            self.assertEqual(chr(data[i + 1].Ascii), c)

        self.process_data(data)

    def process_data(self, data):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        output_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        output_path = os.path.join(output_path, 'kb')
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        f = open(f"{output_path}\\raw_kb.txt", "w+")
        for i, e in enumerate(data):
            f.write(str(i) + '. ' + str(e.__dict__) + '\n')
        f.close()

    def simulate_user(self, text):
        time.sleep(0.5)
        for c in text:
            key_press_duration = random.uniform(0.0001, 0.01)
            self.simulate_press(c, key_press_duration)
            down_to_down = random.uniform(0.0001, 0.15)
            time.sleep(down_to_down)

    def simulate_press(self, character, key_press_duration):
        key = keyboard.KeyCode(char=character)
        self.keyboard_controller.press(key)
        time.sleep(key_press_duration)
        self.keyboard_controller.release(key)


if __name__ == '__main__':
    unittest.main()
