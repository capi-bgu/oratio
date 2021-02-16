import time
import logging
from pynput import mouse
from oratio.collection.DataCollector import DataCollector


class PynputMouseCollector(DataCollector):
    class Event:
        pass

    def __init__(self):
        super().__init__()

    def start_collect(self):
        super().start_collect()
        self.listener = mouse.Listener(
            on_click=self.on_click,
            on_scroll=self.on_scroll,
            on_move=self.on_move)
        self.listener.start()
        logging.info("start kb collecting...")

    def stop_collect(self):
        logging.info("end kb collecting...")
        self.listener.stop()
        return super().stop_collect()

    def on_move(self, x, y):
        event = self.Event()
        event.Timestamp = time.time()
        event.Message = 512
        event.Position = (x, y)
        event.Wheel = 0
        self.data.append(event)

    def on_click(self, x, y, button, pressed):
        event = self.Event()
        event.Timestamp = time.time()
        event.Position = (x, y)
        event.Wheel = 0
        if button == mouse.Button.left:
            if pressed:
                event.Message = 513
            else:
                event.Message = 514
        elif button == mouse.Button.right:
            if pressed:
                event.Message = 516
            else:
                event.Message = 517
        self.data.append(event)

    def on_scroll(self, x, y, dx, dy):
        event = self.Event()
        event.Timestamp = time.time()
        event.Message = 522
        event.Position = (x, y)
        if dy > 0:
            event.Wheel = 1
        elif dy < 0:
            event.Wheel = -1
        self.data.append(event)


if __name__ == '__main__':
    collector = PynputMouseCollector()
    collector.start_collect()
    time.sleep(1000)
    collector.stop_collect()
