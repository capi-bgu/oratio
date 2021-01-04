import os
from src.processing.DataProcessor import DataProcessor


class MouseProcessorStub(DataProcessor):
    def __init__(self):
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/mouse"):
            os.mkdir("../test_output/mouse")
        super().__init__(output_path=r"..\test_output\mouse")

    def process_data(self, data, session):
        f = open(f"{self.output_path}\\s_{session.session_name}_mouse.txt", "w+")
        for i, e in enumerate(data):
            f.write(str(i) + '. ' + str(e.__dict__) + '\n')
