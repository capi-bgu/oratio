import logging
import pickle
import sqlite3
from oratio.database.sqlite_db.SqliteDataHandler import SqliteDataHandler


class CameraDataHandler(SqliteDataHandler):

    def __init__(self, path):
        super().__init__(path)

    def save(self, data):
        """

        :param data: tuple- (session id, list of images- list of np.arrays)
        """
        session, data = data
        data = pickle.dumps(data)

        insert = "INSERT INTO Camera VALUES(?,?)"
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(insert, (session, data))
            connection.commit()
        logging.info("camera data saved")

    def create_data_holder(self, i=-1):
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS Camera \
                        (session BLOB,\
                        Images BLOB,\
                        PRIMARY KEY(session));")
            if i != -1:
                c.execute("DELETE FROM Camera WHERE session >= ?;", (i,))
            connection.commit()
