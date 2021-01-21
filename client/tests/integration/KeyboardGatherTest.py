import json
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
        if not os.path.isdir("../test_output/kb"):
            os.mkdir("../test_output/kb")
        self.out_path = os.path.join(test_dir, 'test_output', 'kb')

        keyboard_processor = KeyboardProcessor()
        keyboard_collector = KeyboardCollector()

        self.st = time.time()
        session = SessionStub(1, 5, self.st)

        st = time.time()
        keyboard_collector.start()
        time.sleep(session.session_duration)
        data = keyboard_collector.stop_collect()
        keyboard_collector.join()
        print(time.time() - st)
        # self.save_data(data)

        st = time.time()
        keyboard_processor.set_arguements(data, session)
        keyboard_processor.start()
        keyboard_processor.join()
        features = keyboard_processor.features
        print(time.time() - st)

        with open(f"{self.out_path}\\integration_test.json", 'w+') as features_file:
            json.dump(features, features_file)


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
