from src.collection.DataCollector import DataCollector
import pyWinhook as pyHook
import pythoncom
import time


class MouseCollector(DataCollector):
    def __init__(self, session, data_processor):
        super().__init__(session, data_processor)
        self.hm = pyHook.HookManager()

    def start_collect(self):
        self.data = []
        self.hook = True
        st = time.time()
        self.hm.MouseAll = self.__mouse_event
        while time.time() - self.session.session_duration < st and self.hook:
            self.hm.HookMouse()
            pythoncom.PumpWaitingMessages()
        self.send_to_process()
        self.stop_collect()

    def stop_collect(self):
        self.hm.UnhookMouse()
        self.hook = False

    def __mouse_event(self, event):
        if not event.Injected:
            event.Timestamp = time.time()
            self.data.append(event)
            return True
        return False
