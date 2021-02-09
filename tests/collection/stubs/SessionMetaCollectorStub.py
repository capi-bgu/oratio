import os
import json
import pathlib
from oratio.collection.DataCollector import DataCollector


class SessionMetaCollectorStub(DataCollector):
    def __init__(self):
        super().__init__()
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.data_path = os.path.join(test_dir, 'test_data', 'session', 'raw_data', 'raw_meta.json')

    def start_collect(self):
        with open(self.data_path, 'r') as test_data:
            self.data = json.loads(test_data.read())

    def stop_collect(self):
        return super().stop_collect()