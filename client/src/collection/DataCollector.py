import threading
import time
from abc import ABC, abstractmethod


class DataCollector(ABC, threading.Thread):

    def __init__(self):
        super().__init__()
        self.collect = True
        self.data = list()

    def run(self):
        self.start_collect()

    @abstractmethod
    def start_collect(self):
        self.collect = True
        self.data = list()

    @abstractmethod
    def stop_collect(self):
        self.collect = False
        return self.data







