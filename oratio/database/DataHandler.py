from abc import ABC, abstractmethod


class DataHandler(ABC):

    def __init__(self, path):
        super().__init__()
        self.path = path

    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def create_data_holder(self, i=-1):
        pass
