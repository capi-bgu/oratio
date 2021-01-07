import time
import pythoncom
import pyWinhook as pyHook
from src.collection.DataCollector import DataCollector


class KeyboardCollector(DataCollector):
    def __init__(self):
        super().__init__()


    def start_collect(self):
        super().start_collect()
        self.hm = pyHook.HookManager()
        self.hm.KeyAll = self.__keyboard_event
        while self.collect:
            self.hm.HookKeyboard()
            pythoncom.PumpWaitingMessages()

    def stop_collect(self):
        self.hm.UnhookKeyboard()
        return super().stop_collect()

    def __keyboard_event(self, event):
        if not event.Injected:
            event.Timestamp = time.time()
            self.data.append(event)
            return True
        return False

