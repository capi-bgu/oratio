from abc import ABC, abstractmethod


class DatabaseManager(ABC):

    def __init__(self, path):
        super().__init__()
        self.path = path

    @abstractmethod
    def create_database(self):
        pass

    @abstractmethod
    def ask(self, query):
        pass