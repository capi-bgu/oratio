import os
from abc import abstractmethod
from src.database.DataHandler import DataHandler


class SqliteDataHandler(DataHandler):

    def __init__(self, path):
        super().__init__(path)
        self.path = path
        self.db_path = os.path.join(self.path, 'capi_client.db')

    @abstractmethod
    def save(self, data):
        pass
