import json
import os
import ast
import time
import pathlib
import unittest
from os import listdir
import pyWinhook as pyHook
from os.path import isfile, join
from tests.SessionStub import SessionStub
from src.processing.MouseProcessor import MouseProcessor


class MouseProcessorTest(unittest.TestCase):
    def test(self):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/mouse"):
            os.mkdir("../test_output/mouse")
        self.out_path = os.path.join(test_dir, 'test_output', 'mouse')
        self.data_path = os.path.join(test_dir, 'test_data', 'mouse')
        self.mpt = MouseProcessor()
        start_time, data = self.__get_data()
        session_duration = 5
        session = SessionStub(0, session_duration, start_time)
        self.mpt.set_arguements(data, session)

        st = time.time()
        self.mpt.start()
        self.mpt.join()
        features = self.mpt.features
        print(time.time() - st)

        with open(f"{self.out_path}\\processor_test.json", 'w+') as features_file:
            json.dump(features, features_file)

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
                    event = pyHook.MouseEvent(event_dict['Message'], event_dict['Position'][0], event_dict['Position'][1],
                                              event_dict['Wheel'], event_dict['Injected'], event_dict['Time'],
                                              event_dict['Window'], event_dict['WindowName'])
                    event.Timestamp = event_dict['Timestamp']
                    data.append(event)
        return start_time, data


if __name__ == '__main__':
    unittest.main()
