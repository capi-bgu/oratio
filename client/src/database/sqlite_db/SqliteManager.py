import os
import sqlite3
from src.database.DatabaseManager import DatabaseManager


class SqliteManager(DatabaseManager):

    def __init__(self, path=""):
        super().__init__(path)
        self.path = path
        self.db_path = os.path.join(self.path, 'data.db')

    def create_database(self):
        with sqlite3.connect(self.db_path) as connection:
            pass
        return super().create_database()


if __name__ == '__main__':
    sql = SqliteManager()
    sql.create_database()
