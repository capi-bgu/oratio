import gc
import time


class Session:
    def __init__(self, session_id, session_duration, data_gatherers, out_path):
        """

        :param session_id: the name of the session
        :param session_duration: number of seconds for session. float
        :param data_gatherers: dictionary for relating collectors to all it's processors,
            and each processor to all it's handlers.
            in the format: {CollectorClass: {ProcessorClass: [DataHandlerClass]}}
        :param out_path: path where we want to save the data. str
        """
        self.session_name = session_id
        self.session_duration = session_duration
        self.out_path = out_path
        self.data_gatherers = dict()
        for collector_class, processor_handlers_dict in data_gatherers.items():
            collector = collector_class()
            self.data_gatherers[collector] = dict()
            for processor_class, handler_classes_list in processor_handlers_dict.items():
                processor = processor_class()
                self.data_gatherers[collector][processor] = list()
                for handler_class in handler_classes_list:
                    self.data_gatherers[collector][processor].append(handler_class(self.out_path))

    def start_session(self):
        print(f"start session {self.session_name}...")
        self.session_start_time = time.time()

        for collector in self.data_gatherers:
            collector.start()
        time.sleep(self.session_duration)
        collected_data = [collector.stop_collect() for collector in self.data_gatherers]
        for collector in self.data_gatherers:
            collector.join()
            del collector

        for i, processor_handlers_dict in enumerate(self.data_gatherers.values()):
            for processor in processor_handlers_dict:
                processor.set_arguements(collected_data[i], self)
                processor.start()
        for processor_handlers_dict in self.data_gatherers.values():
            for processor, handlers_list in processor_handlers_dict.items():
                processor.join()
                for handler in handlers_list:
                    handler.save((self.session_name, processor.features))
                    del handler
                del processor
        del self.data_gatherers
        gc.collect()

    def set_args(self, front_window_type, window_switches, label):
        self.front_window_type = front_window_type
        self.window_switches = window_switches
        self.label = label



