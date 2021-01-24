import gc
import time


class Session:
    def __init__(self, session_id, session_duration, data_gatherers, out_path):
        """

        :param session_id: the name of the session
        :param session_duration: number of seconds for session. float
        :param data_gatherers: dictionary of collectors classes and the list of all related processors classes
            in the format: {CollectorClass: ([*(ProcessorClass, DataHandlerClass)]}. dictionary
        :param out_path: path where we want to save the data. str
        """
        self.session_name = session_id
        self.session_duration = session_duration
        self.out_path = out_path
        self.data_gatherers = dict()
        for collector_class, processor_handler_list in data_gatherers.items():
            collector = collector_class()
            self.data_gatherers[collector] = list()
            for processor_class, handler_class in processor_handler_list:
                self.data_gatherers[collector].append((processor_class(), handler_class(self.out_path)))

    def start_session(self):
        print(f"start session {self.session_name}...")
        self.session_start_time = time.time()

        for collector in self.data_gatherers:
            collector.start()
        time.sleep(self.session_duration)
        all_data = [collector.stop_collect() for collector in self.data_gatherers]
        for collector in self.data_gatherers:
            collector.join()
            del collector

        for i, processor_handler_list in enumerate(self.data_gatherers.values()):
            for processor_handler in processor_handler_list:
                processor = processor_handler[0]
                processor.set_arguements(all_data[i], self)
                processor.start()
        for processor_handler_list in self.data_gatherers.values():
            for processor_handler in processor_handler_list:
                processor = processor_handler[0]
                handler = processor_handler[1]
                processor.join()
                handler.save((self.session_name, processor.features))
                del processor
                del handler
        del self.data_gatherers
        gc.collect()

    def set_args(self, front_window_type, window_switches, label):
        self.front_window_type = front_window_type
        self.window_switches = window_switches
        self.label = label



