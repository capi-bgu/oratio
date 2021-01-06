import os
import pathlib
import time
import unittest
from tests.SessionStub import SessionStub
from src.collection.KeyboardCollector import KeyboardCollector
from src.processing.KeyboardProcessor import KeyboardProcessor


class KeyboardGatherTest(unittest.TestCase):
    def test(self):

        keyboard_processor = KeyboardProcessor("")
        keyboard_collector = KeyboardCollector()
        self.st = time.time()
        session = SessionStub(0, 5, self.st)
        keyboard_collector.start()
        time.sleep(session.session_duration)
        data = keyboard_collector.stop_collect()
        # self.save_data(data)
        features = keyboard_processor.process_data(data, session)
        for k, v in zip(features.keys(), features.values()):
            print(k, v)

    def save_data(self, data):
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/kb"):
            os.mkdir("../test_output/kb")
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        output_path = os.path.join(test_dir, 'test_output', 'kb')

        f = open(f"{output_path}\\_kb.txt", "w+")
        f.write(str(self.st) + '\n')
        for i, e in enumerate(data):
            f.write(str(i) + '. ' + str(e.__dict__) + '\n')
        f.close()



if __name__ == '__main__':
    unittest.main()
