import os
from src.Session import Session
from abc import ABC, abstractmethod


class DataProcessor(ABC):

    def __init__(self, output_path):
        self.output_path = output_path

    @abstractmethod
    def process_data(self, data, session):
        pass



