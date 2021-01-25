import os
import time
import pathlib
import unittest
from src.collection.KeyboardCollector import KeyboardCollector


class KeyboardCollectorTest(unittest.TestCase):
    def test(self):
        self.keyboard_collector = KeyboardCollector()
        self.session_duration = 5
        self.keyboard_collector.start()
        time.sleep(self.session_duration)
        data = self.keyboard_collector.stop_collect()
        self.keyboard_collector.join()

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


if __name__ == '__main__':
    unittest.main()
