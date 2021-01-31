import json
import os
import pathlib

from src.processing.DataProcessor import DataProcessor


class SessionMetaProcessorStub(DataProcessor):

    def __init__(self):
        super().__init__()
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.data_path = os.path.join(test_dir, 'test_data', 'session', 'processed_data', 'processed_meta.json')

    def process_data(self, data=None, session=None):
        self.features = []
        with open(self.data_path) as test_data:
            self.features = json.load(test_data)

        return self.features
