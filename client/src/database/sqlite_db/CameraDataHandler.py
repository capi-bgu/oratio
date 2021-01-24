import os
import sqlite3
from src.database.DataHandelr import DataHandler


class CameraDataHandler(DataHandler):

    def __init__(self, path=""):
        super().__init__(path)
        self.path = path
        self.db_path = os.path.join(self.path, 'data.db')
        self.create_table()

    def save(self, data):
        pass

    def ask(self, query):
        pass

    def create_table(self):
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS Images \
                        (session BLOB,\
                        Images BLOB,\
                        PRIMARY KEY(session));")

