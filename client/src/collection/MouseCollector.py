import time
import logging
import pythoncom
import pyWinhook as pyHook
from src.collection.DataCollector import DataCollector


class MouseCollector(DataCollector):

    def __init__(self):
        super().__init__()
        self.hm = pyHook.HookManager()

    def start_collect(self):
        logging.info("start mouse collecting...")
        super().start_collect()
        self.hm.MouseAll = self.__mouse_event
        self.hm.HookMouse()
        while self.collect:
            pythoncom.PumpWaitingMessages()
            time.sleep(0.001)
        logging.info("end mouse collecting...")

    def stop_collect(self):
        self.hm.UnhookMouse()
        return super().stop_collect()

    def __mouse_event(self, event):
        event.Timestamp = time.time()
        self.data.append(event)
        return True
