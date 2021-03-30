import time
import psutil
import logging
import win32gui
import win32process
from oratio.collection.DataCollector import DataCollector
from threading import Condition, Lock


class SessionMetaCollector(DataCollector):

    def __init__(self, record_window=0.333):
        super().__init__()
        self.record_window = record_window
        self.waiter = Condition(Lock())

    def start_collect(self):
        logging.info("start metadata collecting...")
        self.waiter.acquire(True)
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
            self.waiter.wait(self.record_window)
            #time.sleep(self.record_window)
        self.waiter.release()
        logging.info("end metadata collecting...")

    def stop_collect(self):
        self.waiter.acquire(True)
        data = super().stop_collect()
        self.waiter.notify()
        self.waiter.release()
        return data
