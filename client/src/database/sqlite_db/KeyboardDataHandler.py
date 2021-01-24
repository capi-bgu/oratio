import os
import sqlite3
from src.database.DataHandelr import DataHandler


class KeyboardDataHandler(DataHandler):

    def __init__(self, path=""):
        super().__init__(path)
        self.path = path
        self.db_path = os.path.join(self.path, 'data.db')
        self.create_table()

    def save(self, data):
        pass

    def ask(self, query):
        pass

    def create_table(self):
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
                        uppercase_counter REAL ,\
                        digraph_duration NUMERIC ,\
                        trigraph_duration NUMERIC ,\
                        mode_key REAL ,\
                        idle_time NUMERIC ,\
                        unique_events REAL ,\
                        PRIMARY KEY(session));")

