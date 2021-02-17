import os
import ast
import pathlib
from os import listdir
from os.path import isfile, join
from oratio.collection.DataCollector import DataCollector


class KeyboardCollectorStub(DataCollector):
    class Event:
        pass

    def __init__(self):
        super().__init__()
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.data_path = os.path.join(test_dir, 'test_data', 'kb', 'raw_data')

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
                    event = self.Event()
                    event.Message = event_dict['Message']
                    event.KeyID = event_dict['KeyID']
                    event.Key = event_dict['Key']
                    event.Timestamp = event_dict['Timestamp']
                    data.append(event)
        return start_time, data


if __name__ == '__main__':
    keyboard_collector_stub = KeyboardCollectorStub()
    st, data = keyboard_collector_stub.stop_collect()
    print(st, data)
