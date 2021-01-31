import os
import sqlite3
from src.database.DatabaseManager import DatabaseManager


class SqliteManager(DatabaseManager):

    def __init__(self, path=""):
        super().__init__(path)
        self.db_path = os.path.join(self.path, 'data.db')

    def create_database(self):
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        with sqlite3.connect(self.db_path) as connection:
            pass

    def ask(self, query):
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(query)
            return c.fetchall()


if __name__ == '__main__':
    sql = SqliteManager()
    sql.create_database()
