from abc import ABC, abstractmethod


class DataCollector(ABC):

    def __init__(self):
        super().__init__()
        self.collect = True
        self.data = list()

    @abstractmethod
    def start_collect(self):
        self.collect = True
        self.data = list()

    @abstractmethod
    def stop_collect(self):
        self.collect = False
        return self.data







