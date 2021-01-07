import time
import pythoncom
import pyWinhook as pyHook
from src.collection.DataCollector import DataCollector


class MouseCollector(DataCollector):
    def __init__(self):
        super().__init__()

    def start_collect(self):
        super().start_collect()
        self.hm = pyHook.HookManager()
        self.hm.MouseAll = self.__mouse_event
        while self.collect:
            self.hm.HookMouse()
            pythoncom.PumpWaitingMessages()
        # self.stop_collect()

    def stop_collect(self):
        self.hm.UnhookMouse()
        return super().stop_collect()

    def __mouse_event(self, event):
        if not event.Injected:
            event.Timestamp = time.time()
            self.data.append(event)
            return True
        return False
