import time
import psutil
import logging
import win32gui
import win32process
from oratio.collection.DataCollector import DataCollector


class SessionMetaCollector(DataCollector):

    def __init__(self, record_window=0.333):
        super().__init__()
        self.record_window = record_window

    def start_collect(self):
        logging.info("start metadata collecting...")
        super().start_collect()
        while self.collect:
            try:
                window_handle = win32gui.GetForegroundWindow()
                pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())

                window_process_name = psutil.Process(pid[-1]).name()
                window_title = str(repr(win32gui.GetWindowText(window_handle)))
            except Exception as e:
                logging.error(e)
                window_process_name = "Unknown"
                window_title = "Unknown"

            self.data.append((window_process_name, window_title))
            time.sleep(self.record_window)
        logging.info("end metadata collecting...")

    def stop_collect(self):
        return super().stop_collect()
