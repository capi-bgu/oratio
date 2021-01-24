import os
import sqlite3
from abc import ABC, abstractmethod
from src.database.DataHandelr import DataHandler


class SqliteDataHandler(ABC, DataHandler):

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

    def ask(self, query):
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(query)
            return c.fetchall()

    @abstractmethod
    def create_table(self):
        pass
