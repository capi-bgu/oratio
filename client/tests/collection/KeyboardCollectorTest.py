import os
import time
import pathlib
import unittest
from src.collection.KeyboardCollector import KeyboardCollector


class KeyboardCollectorTest(unittest.TestCase):
    def test(self):
        self.keyboard_collector = KeyboardCollector()
        self.keyboard_collector.start()
        self.session_duration = 5
        time.sleep(self.session_duration)
        data = self.keyboard_collector.stop_collect()
        self.process_data(data)

    def process_data(self, data):
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/kb"):
            os.mkdir("../test_output/kb")
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        output_path = os.path.join(test_dir, 'test_output', 'kb')
        f = open(f"{output_path}\\_kb.txt", "w+")
        for i, e in enumerate(data):
            f.write(str(i) + '. ' + str(e.__dict__) + '\n')
        f.close()


if __name__ == '__main__':
    unittest.main()
