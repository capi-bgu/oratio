import os
import ast
import time
import pathlib
import unittest
from os import listdir
import pyWinhook as pyHook
from os.path import isfile, join
from tests.SessionStub import SessionStub
from src.processing.KeyboardProcessor import KeyboardProcessor


class KeyboardProcessorTest(unittest.TestCase):
    def test(self):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()

        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")

        self.out_path = os.path.join(test_dir, 'test_output')
        self.data_path = os.path.join(test_dir, 'test_data', 'kb')
        self.kbpt = KeyboardProcessor(self.out_path)
        start_time, data = self.__get_data()
        st = time.time()
        self.kbpt.process_data(data, SessionStub(0, 5, start_time))
        print(time.time() - st)

    def __get_data(self):
        data = []
        files = [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]
        data_file = files[0]
        with open(self.data_path + '\\' + data_file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if i == 0:
                    start_time = float(line)
                else:
                    event_str = '{' + line.split('{')[1]
                    event_str = event_str.replace("\'", "\"")
                    event_dict = ast.literal_eval(event_str)
                    event = pyHook.KeyboardEvent(event_dict['Message'], event_dict['KeyID'], event_dict['ScanCode'],
                                                 event_dict['Ascii'], event_dict['flags'], event_dict['Time'],
                                                 event_dict['Window'], event_dict['WindowName'])
                    event.Timestamp = event_dict['Timestamp']
                    data.append(event)
        return start_time, data


if __name__ == '__main__':
    unittest.main()
