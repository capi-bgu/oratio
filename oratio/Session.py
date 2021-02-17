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
        self.data_gatherers = data_gatherers
        self.start_time = 0
        self.label = -1

    def start_session(self):
        logging.info("************************\n")
        logging.info(f"start session {self.id}...")
        self.start_time = time.time()
        raw_data = self.__collect()
        Thread(target=self.__process_and_save, args=(raw_data,)).start()
        logging.info("************************\n")

    def __collect(self):
        collectors_threads = list()
        for collector in self.data_gatherers:
            collectors_threads.append(Thread(target=collector.start_collect))
        for collector in collectors_threads:
            collector.start()
        time.sleep(self.duration)
        raw_data = [collector.stop_collect() for collector in self.data_gatherers]
        for collector in collectors_threads:
            collector.join()
        return raw_data

    def __process_and_save(self, raw_data):
        for i, processor_handlers_dict in enumerate(self.data_gatherers.values()):
            for processor in processor_handlers_dict:
                processor.process_data(raw_data[i], self)

        for processor_handlers_dict in self.data_gatherers.values():
            for processor, handlers_list in processor_handlers_dict.items():
                for handler in handlers_list:
                    handler.save((self.id, processor.features))

    def set_label(self, label):
        self.label = label



