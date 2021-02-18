import logging
from abc import abstractmethod
from oratio.database.DataHandler import DataHandler

class DatabaseManager(DataHandler):

    def __init__(self, path):
        super().__init__(path)
        self.path = path

    def save(self, data):
        if type(data) == tuple:
            logging.error("DatabaseManager can only save Session data")
        self.save_session(data)

    @abstractmethod
    def save_session(self, session):
        pass

    @abstractmethod
    def create_data_holder(self, i=-1):
        pass

    @abstractmethod
    def ask(self, query):
        pass

    @abstractmethod
    def __len__(self):
        pass
