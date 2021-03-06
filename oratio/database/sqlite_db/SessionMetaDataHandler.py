import logging
import sqlite3
from oratio.database.sqlite_db.SqliteDataHandler import SqliteDataHandler


class SessionMetaDataHandler(SqliteDataHandler):

    def __init__(self, path):
        super().__init__(path)

    def save(self, data):
        """

        :param data: tuple - (session name, data dictionary)
        """

        session, data = data

        insert = "INSERT INTO SessionMeta VALUES(?,?,?,?,?,?,?)"
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(insert, (session,
                               data["dominate_window"],
                               data["dominate_task"],
                               data["window_switches"],
                               data["task_switches"],
                               data["window_count"],
                               data["task_count"]))

            connection.commit()
        logging.info("meta data saved")


    def create_data_holder(self, i=-1):
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS SessionMeta \
                        (session BLOB ,\
                        dominate_window TEXT,\
                        dominate_task TEXT, \
                        window_switches REAL, \
                        task_switches REAL, \
                        window_count REAL, \
                        task_count REAL, \
                        PRIMARY KEY(session));")

            if i != -1:
                c.execute("DELETE FROM SessionMeta WHERE session >= ?", (i,))
            connection.commit()


