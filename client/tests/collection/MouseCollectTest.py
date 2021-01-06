import os
import time
import pathlib
import unittest
from src.collection.MouseCollector import MouseCollector


class MouseCollectorTest(unittest.TestCase):
    def test(self):
        self.mouse_collector = MouseCollector()
        self.mouse_collector.start()
        self.session_duration = 5
        time.sleep(self.session_duration)
        data = self.mouse_collector.stop_collect()
        self.process_data(data)

    def process_data(self, data):
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/mouse"):
            os.mkdir("../test_output/mouse")
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        output_path = os.path.join(test_dir, 'test_output', 'mouse')
        f = open(f"{output_path}\\_mouse.txt", "w+")
        for i, e in enumerate(data):
            f.write(str(i) + '. ' + str(e.__dict__) + '\n')
        f.close()


if __name__ == '__main__':
    unittest.main()
