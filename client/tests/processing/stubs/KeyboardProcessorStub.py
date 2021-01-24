import json
import os
import pathlib
from src.processing.DataProcessor import DataProcessor


class KeyboardProcessorStub(DataProcessor):
    def __init__(self):
        super().__init__()
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.data_path = os.path.join(test_dir, 'test_data', 'kb', 'processed_data')

    def process_data(self, data="", session=""):
        with open(self.data_path + '\\' + 'processed_kb.json') as json_file:
            features_data = json.load(json_file)
        self.features = features_data
        return self.features


if __name__ == '__main__':
    features = KeyboardProcessorStub().process_data()
    print(features)
