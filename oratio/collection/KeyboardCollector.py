import time
import logging
from pynput import keyboard
from oratio.collection.DataCollector import DataCollector


class KeyboardCollector(DataCollector):
    class Event:
        pass

    def __init__(self):
        super().__init__()

    def start_collect(self):
        super().start_collect()
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()
        logging.info("start kb collecting...")

    def stop_collect(self):
        logging.info("end kb collecting...")
        self.listener.stop()
        return super().stop_collect()

    def on_press(self, key):
        event = self.Event()
        event.Timestamp = time.time()
        event.Message = 256
        if isinstance(key, keyboard.KeyCode):  # it's a button with char
            event.KeyID = key.vk
            event.Key = key.char
        else:  # modifier
            event.KeyID = key.value.vk
            event.Key = key.name
        self.data.append(event)

    def on_release(self, key):
        event = self.Event()
        event.Timestamp = time.time()
        event.Message = 257
        if isinstance(key, keyboard.KeyCode):  # it's a button with char
            event.KeyID = key.vk
            event.Key = key.char
        else:
            event.KeyID = key.value.vk
            event.Key = key.name
        self.data.append(event)


if __name__ == '__main__':
    collector = KeyboardCollector()
    collector.start_collect()
    time.sleep(1000)
    collector.stop_collect()