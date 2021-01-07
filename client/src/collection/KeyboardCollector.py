import time
import pythoncom
import pyWinhook as pyHook
from src.collection.DataCollector import DataCollector


class KeyboardCollector(DataCollector):
    #hm = pyHook.HookManager()

    def __init__(self):
        super().__init__()
        self.hm = pyHook.HookManager()


    def start_collect(self):
        print("start kb collecting...")
        super().start_collect()
        self.hm.KeyAll = self.__keyboard_event
        self.hm.HookKeyboard()
        while self.collect:
            pythoncom.PumpWaitingMessages()
        print("end kb collecting...")

    def stop_collect(self):
        self.hm.UnhookKeyboard()
        return super().stop_collect()

    def __keyboard_event(self, event):
        if not event.Injected:
            event.Timestamp = time.time()
            self.data.append(event)
            return True
        return False

