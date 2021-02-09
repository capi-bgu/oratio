from abc import ABC, abstractmethod


class DataProcessor(ABC):

    def __init__(self):
        super().__init__()
        self.features = None

    @abstractmethod
    def process_data(self, data, session):
        pass
