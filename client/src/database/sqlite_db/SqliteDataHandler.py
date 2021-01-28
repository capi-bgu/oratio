import os
import sqlite3
from abc import abstractmethod
from src.database.DataHandelr import DataHandler


class SqliteDataHandler(DataHandler):

    def __init__(self, path=""):
        super().__init__(path)
        self.path = path
        self.db_path = os.path.join(self.path, 'data.db')
        self.create_table()

    @abstractmethod
    def save(self, data):
        """

        :param data: tuple- (session name, features dataa)
        """
        session = data[0]
        data = data[1]
        return str(session), data

    @abstractmethod
    def create_table(self):
        pass

