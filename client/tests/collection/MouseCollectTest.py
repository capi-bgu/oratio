import os
import time
import pathlib
import unittest
from src.collection.MouseCollector import MouseCollector


class MouseCollectorTest(unittest.TestCase):
    def test(self):
        self.mouse_collector = MouseCollector()
        self.session_duration = 5
        self.mouse_collector.start()
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


if __name__ == '__main__':
    unittest.main()
