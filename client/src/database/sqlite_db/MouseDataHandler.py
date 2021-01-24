import os
import sqlite3
from src.database.DataHandelr import DataHandler

class MouseDataHandler(DataHandler):

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
            c.execute("CREATE TABLE IF NOT EXISTS Mouse \
                        (session BLOB ,\
                        right_click_count REAL , \
                        left_click_count REAL , \
                        scroll_speed NUMERIC , \
                        double_click_count REAL , \
                        cursor_x_distance NUMERIC , \
                        cursor_y_distance NUMERIC , \
                        average_momentary_speed_x NUMERIC , \
                        average_momentary_speed_y NUMERIC , \
                        average_speed_x NUMERIC , \
                        average_speed_y NUMERIC , \
                        average_active_speed_x NUMERIC , \
                        average_active_speed_y NUMERIC , \
                        average_cursor_x_angle NUMERIC , \
                        average_cursor_y_angle NUMERIC , \
                        cursor_distance_ratio NUMERIC , \
                        idle_time NUMERIC , \
                        right_click_duration NUMERIC , \
                        left_click_duration NUMERIC , \
                        PRIMARY KEY(session));")

