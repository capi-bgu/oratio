from src.processing.DataProcessor import DataProcessor


class MouseProcessor(DataProcessor):
    def __init__(self, output_path):
        super().__init__(output_path)

    def process_data(self, data, session):
        super().process_data(data, session)