import os
import pathlib
import time
import unittest
from tests.SessionStub import SessionStub
from src.collection.KeyboardCollector import KeyboardCollector
from src.processing.KeyboardProcessor import KeyboardProcessor


class KeyboardGatherTest(unittest.TestCase):
    def test(self):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        out_path = os.path.join(test_dir, 'test_output')

        keyboard_processor = KeyboardProcessor(out_path)
        keyboard_collector = KeyboardCollector()
        self.st = time.time()
        session = SessionStub(1, 5, self.st)
        keyboard_collector.start()
        time.sleep(session.session_duration)
        data = keyboard_collector.stop_collect()
        # self.save_data(data)
        keyboard_processor.process_data(data, session)


    def save_data(self, data):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        output_path = os.path.join(test_dir, 'test_output', 'kb')

        f = open(f"{output_path}\\_kb.txt", "w+")
        f.write(str(self.st) + '\n')
        for i, e in enumerate(data):
            f.write(str(i) + '. ' + str(e.__dict__) + '\n')
        f.close()



if __name__ == '__main__':
    unittest.main()
