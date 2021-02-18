import logging
import os
import sqlite3
from oratio.database.DatabaseManager import DatabaseManager


class SqliteManager(DatabaseManager):

    def __init__(self, path=""):
        super().__init__(path)
        self.db_path = os.path.join(self.path, 'capi_client.db')

    def ask(self, query):
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(query)
            return c.fetchall()

    def save_session(self, session):
        insert = "INSERT INTO Session VALUES(?,?,?)"
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(insert, (str(session.id),
                               session.start_time,
                               str(session.label)))
            connection.commit()
        logging.info("session data saved")

    def create_data_holder(self, i=-1):
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS Session \
                        (session BLOB ,\
                        time BLOB,\
                        label BLOB,\
                        PRIMARY KEY(session));")

    def __len__(self):
        return self.ask("SELECT COUNT(session) FROM Session")[0][0]
