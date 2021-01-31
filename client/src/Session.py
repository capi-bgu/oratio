import gc
import time
from threading import Thread


class Session:
    def __init__(self, session_id, session_duration, data_gatherers, out_path):
        """

        :param session_id: the name of the session
        :param session_duration: number of seconds for session. float
        :param data_gatherers: dictionary for relating collectors to all it's processors,
            and each processor to all it's handlers.
            in the format: {CollectorC: {Processor: [DataHandler]}}
        :param out_path: path where we want to save the data. str
        """
        self.session_name = session_id
        self.session_duration = session_duration
        self.out_path = out_path
        self.data_gatherers = data_gatherers

    def start_session(self):
        print(f"start session {self.session_name}...")
        self.session_start_time = time.time()
        collectors_threads = list()
        for collector in self.data_gatherers:
            collectors_threads.append(Thread(target=collector.start_collect))
        for collector in collectors_threads:
            collector.start()
        time.sleep(self.session_duration)
        collected_data = [collector.stop_collect() for collector in self.data_gatherers]
        for collector in collectors_threads:
            collector.join()

        processors_threads = list()
        for i, processor_handlers_dict in enumerate(self.data_gatherers.values()):
            for processor in processor_handlers_dict:
                processors_threads.append(Thread(target=processor.process_data, args=(collected_data[i], self)))
        for processor in processors_threads:
            processor.start()
        for processor in processors_threads:
            processor.join()
        for processor_handlers_dict in self.data_gatherers.values():
            for processor, handlers_list in processor_handlers_dict.items():
                for handler in handlers_list:
                    handler.save((self.session_name, processor.features))

    def set_args(self, front_window_type, window_switches, label):
        self.front_window_type = front_window_type
        self.window_switches = window_switches
        self.label = label



