import os
import pathlib
import time
import unittest
from tests.SessionStub import SessionStub
from src.collection.MouseCollector import MouseCollector
from src.processing.MouseProcessor import MouseProcessor


class MouseGatherTest(unittest.TestCase):
    def test(self):

        mouse_processor = MouseProcessor("")
        mouse_collector = MouseCollector()
        self.st = time.time()
        mouse_collector.start()
        session = SessionStub(0, 5, self.st)
        time.sleep(session.session_duration)
        data = mouse_collector.stop_collect()
        # self.save_data(data)
        features = mouse_processor.process_data(data, session)
        for k, v in zip(features.keys(), features.values()):
            print(k, v)

    def save_data(self, data):
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/mouse"):
            os.mkdir("../test_output/mouse")
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        output_path = os.path.join(test_dir, 'test_output', 'mouse')

        f = open(f"{output_path}\\_mouse.txt", "w+")
        f.write(str(self.st) + '\n')
        for i, e in enumerate(data):
            f.write(str(i) + '. ' + str(e.__dict__) + '\n')
        f.close()


if __name__ == '__main__':
    unittest.main()
