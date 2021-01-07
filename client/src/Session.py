import gc
import time


class Session:
    def __init__(self, session_id, session_duration, data_gatherers, out_path):
        """

        :param session_id: the name of the session
        :param session_duration: required session duration
        :param data_gatherers: dictionary of collectors classes and the list of all related processors classes
            in the format: {CollectorClass: [*ProcessorClass]}
        """
        self.session_name = session_id
        self.session_duration = session_duration
        self.session_start_time = time.time()
        self.data_gatherers = dict()
        for collector_class, processors_class in data_gatherers.items():
            collector = collector_class()
            self.data_gatherers[collector] = list()
            for processor_class in processors_class:
                self.data_gatherers[collector].append(processor_class(out_path))

    def start_session(self):
        print(f"start session {self.session_name}...")
        for collector in self.data_gatherers:
            collector.start()
        time.sleep(self.session_duration)
        for collector, processors in self.data_gatherers.items():
            data = collector.stop_collect()
            del collector
            for processor in processors:
                processor.process_data(data, self)
                del processor
        del self.data_gatherers
        gc.collect()
