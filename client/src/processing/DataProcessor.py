from abc import ABC, abstractmethod
from src.Session import Session
import os


class DataProcessor(ABC):

    def __init__(self, output_path: str):
        self.output_path = output_path

    @abstractmethod
    def process_data(self, data: list, session: Session):
        os.chdir(self.output_path)




