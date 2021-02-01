import sqlite3
from src.database.sqlite_db.SqliteDataHandler import SqliteDataHandler


class SessionDataHandler(SqliteDataHandler):

    def __init__(self, path):
        super().__init__(path)

    def save(self, data):
        """

        :param data: Session
        """

        insert = "INSERT INTO Session VALUES(?,?,?)"
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(insert, (str(data.id),
                               data.start_time,
                               str(data.label)))
            connection.commit()

    def create_data_holder(self):
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS Session \
                        (session BLOB ,\
                        time BLOB,\
                        PRIMARY KEY(session));")
