import pickle
import sqlite3
from src.database.sqlite_db.SqliteDataHandler import SqliteDataHandler


class RawDataHandler(SqliteDataHandler):

    def __init__(self, name, path):
        super().__init__(path)
        self.name = name

    def save(self, data):
        """

        :param data: tuple- (session name, list of all events in session)
        """
        session, data = data
        data = pickle.dumps(data)

        insert = f"INSERT INTO {self.name} VALUES(?,?)"
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(insert, (session, data))
            connection.commit()

    def create_data_holder(self):
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(f"CREATE TABLE IF NOT EXISTS {self.name} \
                        (session BLOB ,\
                        events BLOB, \
                        PRIMARY KEY(session));")

