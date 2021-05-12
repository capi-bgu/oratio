import logging
import sqlite3
from oratio.database.sqlite_db.SqliteDataHandler import SqliteDataHandler


class MouseDataHandler(SqliteDataHandler):

    def __init__(self, path):
        super().__init__(path)

    def save(self, data):
        """

        :param data: tuple- (session id, dictionary of all keyboard features from mouse processor)
        """
        session, data = data

        insert = "INSERT INTO Mouse VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        with sqlite3.connect(self.db_path) as connection:
            c = connection.cursor()
            c.execute(insert, (session,
                               data['right_click_count'],
                               data['left_click_count'],
                               data['scroll_speed'],
                               data['double_click_count'],
                               data['cursor_x_distance'],
                               data['cursor_y_distance'],
                               data['average_momentary_speed_x'],
                               data['average_momentary_speed_y'],
                               data['average_speed_x'],
                               data['average_speed_y'],
                               data['average_active_speed_x'],
                               data['average_active_speed_y'],
                               data['average_cursor_angle'],
                               data['speed_std'],
                               data['std_cursor_angle'],
                               data['Turn_0_45'],
                               data['Turn_45_90'],
                               data['Turn_90_135'],
                               data['Turn_135_180'],
                               data['Direction_S'],
                               data['Direction_SW'],
                               data['Direction_W'],
                               data['Direction_NW'],
                               data['Direction_N'],
                               data['Direction_NE'],
                               data['Direction_E'],
                               data['Direction_SE'],
                               data['Dist1'],
                               data['Dist2'],
                               data['Dist3'],
                               data['idle_time'],
                               data['right_click_duration'],
                               data['left_click_duration']))
            connection.commit()
        logging.info("mouse data saved")

    def create_data_holder(self, i=-1):
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
                        average_cursor_angle NUMERIC , \
                        speed_std NUMERIC , \
                        std_cursor_angle NUMERIC , \
                        Turn_0_45 NUMERIC , \
                        Turn_45_90 NUMERIC , \
                        Turn_90_135 NUMERIC , \
                        Turn_135_180 NUMERIC , \
                        Direction_S NUMERIC , \
                        Direction_SW NUMERIC , \
                        Direction_W NUMERIC , \
                        Direction_NW NUMERIC , \
                        Direction_N NUMERIC , \
                        Direction_NE NUMERIC , \
                        Direction_E NUMERIC , \
                        Direction_SE NUMERIC , \
                        Dist1 NUMERIC , \
                        Dist2 NUMERIC , \
                        Dist3 NUMERIC , \
                        idle_time NUMERIC , \
                        right_click_duration NUMERIC , \
                        left_click_duration NUMERIC , \
                        PRIMARY KEY(session));")

            if i != -1:
                c.execute("DELETE FROM Mouse WHERE session >= ?", (i,))
            connection.commit()