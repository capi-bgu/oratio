import os
import sqlite3
import numpy as np
import msgpack
import msgpack_numpy as m
from src.database.sqlite_db.SqliteDataHandler import SqliteDataHandler


class CameraDataHandler(SqliteDataHandler):

    def __init__(self, path=""):
        super().__init__(path)

    def save(self, data):
        """

        :param data: tuple- (session name, list of images- list of np.arrays)
        """
        session, data = super().save(data)

        data = np.array(data)
        data = msgpack.packb(data, default=m.encode)

        insert = "INSERT INTO Images VALUES(?,?)"
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(insert, (session, data))
            connection.commit()

    def create_table(self):
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS Images \
                        (session BLOB,\
                        Images BLOB,\
                        PRIMARY KEY(session));")
