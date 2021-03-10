import logging
import pickle
import sqlite3
from oratio.database.sqlite_db.SqliteDataHandler import SqliteDataHandler


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
        logging.info(f"{self.name} data saved")


    def create_data_holder(self, i=-1):
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(f"CREATE TABLE IF NOT EXISTS {self.name} \
                        (session BLOB ,\
                        data BLOB, \
                        PRIMARY KEY(session));")

            if i != -1:
                c.execute(f"DELETE FROM {self.name} WHERE session >= ?", (i,))
            connection.commit()
