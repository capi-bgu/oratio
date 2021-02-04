import time
import logging
from threading import Thread


class Session:
    def __init__(self, id, duration, data_gatherers, out_path):
        """

        :param id: the id of the session
        :param duration: number of seconds for session. float
        :param data_gatherers: dictionary for relating collectors to all it's processors,
            and each processor to all it's handlers.
            in the format: {CollectorC: {Processor: [DataHandler]}}
        :param out_path: path where we want to save the data. str
        """
        self.id = id
        self.duration = duration
        self.out_path = out_path

        self.collector_processor = {}
        self.processor_handler = {}

        for collector, processor_handlers in data_gatherers.items():
            self.collector_processor[collector] = list(processor_handlers.keys())
            self.processor_handler.update(processor_handlers)

    def start_session(self):
        logging.info(f"start session {self.id}...")
        self.start_time = time.time()

        collectors_threads = list()
        for collector in self.collector_processor:
            collectors_threads.append(Thread(target=self.__collecting, args=(collector,)))
        for collector in collectors_threads:
            collector.start()
        for collector in collectors_threads:
            collector.join()
        logging.info("***************************\n")

    def __collecting(self, collector):
        collector_thread = Thread(target=collector.start_collect)
        collector_thread.start()
        time.sleep(self.duration)
        collected_date = collector.stop_collect()
        collector_thread.join()

        for processor in self.collector_processor[collector]:
            Thread(target=self.__processing_saving, args=(processor, collected_date)).start()

    def __processing_saving(self, processor, data):
        processor.process_data(data, self)

        for handler in self.processor_handler[processor]:
            Thread(target=handler.save, args=((self.id, processor.features),)).start()

    def set_label(self, label):
        self.label = label



