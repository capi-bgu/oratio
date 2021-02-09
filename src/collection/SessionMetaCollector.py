import time
import psutil
import logging
import win32gui
import win32process
from src.collection.DataCollector import DataCollector


class SessionMetaCollector(DataCollector):

    def __init__(self, record_window=0.333):
        super().__init__()
        self.record_window = record_window

    def start_collect(self):
        logging.info("starting to collect session metadata...")
        super().start_collect()
        while self.collect:
            window_handle = win32gui.GetForegroundWindow()
            pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())

            window_process_name = psutil.Process(pid[-1]).name()
            window_title = str(repr(win32gui.GetWindowText(window_handle)))

            self.data.append((window_process_name, window_title))
            time.sleep(self.record_window)

    def stop_collect(self):
        return super().stop_collect()
