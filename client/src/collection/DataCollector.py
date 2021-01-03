from abc import ABC, abstractmethod
from src.processing.DataProcessor import DataProcessor
from src.Session import Session


class DataCollector(ABC):

    def __init__(self, session: Session, data_processor: DataProcessor):
        """

        :param session: The active session
        :param data_processor: The processor that we give the data to
        """
        self.session = session
        self.data_processor = data_processor
        self.data = None

    @abstractmethod
    def start_collect(self):
        pass

    @abstractmethod
    def stop_collect(self):
        pass

    def send_to_process(self):
        self.data_processor.process_data(self.data, self.session)
