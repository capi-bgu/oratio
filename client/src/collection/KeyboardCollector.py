from src.collection.DataCollector import DataCollector
import pyWinhook as pyHook
import pythoncom
import time


class KeyboardCollector(DataCollector):
    def __init__(self, session, data_processor):
        super().__init__(session, data_processor)
        self.hm = pyHook.HookManager()

    def start_collect(self):
        self.data = []
        self.hook = True
        st = time.time()
        self.hm.KeyAll = self.__keyboard_event
        while time.time() - self.session.session_duration < st and self.hook:
            self.hm.HookKeyboard()
            pythoncom.PumpWaitingMessages()
        self.send_to_process()
        self.stop_collect()

    def stop_collect(self):
        self.hm.UnhookKeyboard()
        self.hook = False

    def __keyboard_event(self, event):
        if not event.Injected:
            self.data.append(event)
            print(event.Key)
            return True
        return False
