import ast
import os
import pathlib
from os import listdir
from os.path import isfile, join
from src.collection.DataCollector import DataCollector
import pyWinhook as pyHook


class MouseCollectorStub(DataCollector):
    def __init__(self):
        super().__init__()
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.data_path = os.path.join(test_dir, 'test_data', 'mouse', 'raw_data')

    def start_collect(self):
        pass

    def stop_collect(self):
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
                    event = pyHook.MouseEvent(event_dict['Message'], event_dict['Position'][0],
                                              event_dict['Position'][1],
                                              event_dict['Wheel'], event_dict['Injected'], event_dict['Time'],
                                              event_dict['Window'], event_dict['WindowName'])
                    event.Timestamp = event_dict['Timestamp']
                    data.append(event)
        return start_time, data
