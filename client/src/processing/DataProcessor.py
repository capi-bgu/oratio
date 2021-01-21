import os
import threading

from src.Session import Session
from abc import ABC, abstractmethod


class DataProcessor(ABC, threading.Thread):

    def __init__(self):
        super().__init__()
        self.features = None

    @abstractmethod
    def process_data(self, data, session):
        pass

    def run(self):
        self.process_data(self.data, self.session)

    def set_arguements(self, data, session):
        self.data = data
        self.session = session
