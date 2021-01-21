import json
import os
import pathlib
import time
import unittest
from tests.SessionStub import SessionStub
from src.collection.MouseCollector import MouseCollector
from src.processing.MouseProcessor import MouseProcessor


class MouseGatherTest(unittest.TestCase):
    def test(self):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/mouse"):
            os.mkdir("../test_output/mouse")
        self.out_path = os.path.join(test_dir, 'test_output', 'mouse')

        mouse_processor = MouseProcessor()
        mouse_collector = MouseCollector()

        self.st = time.time()
        session = SessionStub(1, 5, self.st)

        st = time.time()
        mouse_collector.start()
        time.sleep(session.session_duration)
        data = mouse_collector.stop_collect()
        mouse_collector.join()
        print(time.time() - st)
        # self.save_data(data)

        st = time.time()
        mouse_processor.set_arguements(data, session)
        mouse_processor.start()
        mouse_processor.join()
        features = mouse_processor.features
        print(time.time() - st)

        with open(f"{self.out_path}\\integration_test.json", 'w+') as features_file:
            json.dump(features, features_file)

    def save_data(self, data):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        output_path = os.path.join(test_dir, 'test_output', 'mouse')

        f = open(f"{output_path}\\_mouse.txt", "w+")
        f.write(str(self.st) + '\n')
        for i, e in enumerate(data):
            f.write(str(i) + '. ' + str(e.__dict__) + '\n')
        f.close()


if __name__ == '__main__':
    unittest.main()
