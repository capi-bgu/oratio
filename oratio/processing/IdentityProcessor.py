from oratio.processing.DataProcessor import DataProcessor

class IdentityProcessor(DataProcessor):
    def process_data(self, data, session):
        self.features = data
        return self.features
