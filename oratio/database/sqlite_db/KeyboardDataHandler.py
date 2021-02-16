import sqlite3
from oratio.database.sqlite_db.SqliteDataHandler import SqliteDataHandler


class KeyboardDataHandler(SqliteDataHandler):

    def __init__(self, path):
        super().__init__(path)

    def save(self, data):
        """

        :param data: tuple- (session id, dictionary of all keyboard features from keyboard processor)
        """
        session, data = data

        insert = "INSERT INTO Keyboard VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(insert, (session,
                               data['typing_speed'],
                               data['active_typing_speed'],
                               data['average_press_duration'],
                               data['average_down_to_down'],
                               data['regular_press_count'],
                               data['punctuations_press_count'],
                               data['space_counter'],
                               data['error_corrections'],
                               data['mode_key'],
                               data['idle_time'],
                               data['unique_events']))
            connection.commit()

    def create_data_holder(self):
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS Keyboard \
                        (session BLOB ,\
                        typing_speed NUMERIC ,\
                        average_press_duration NUMERIC ,\
                        average_down_to_down NUMERIC ,\
                        regular_press_count REAL ,\
                        punctuations_press_count REAL ,\
                        space_counter REAL ,\
                        special_press_count REAL ,\
                        error_corrections REAL ,\
                        mode_key REAL ,\
                        idle_time NUMERIC ,\
                        unique_events REAL ,\
                        PRIMARY KEY(session));")

