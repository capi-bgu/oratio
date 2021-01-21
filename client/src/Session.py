import gc
import json
import os
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
        self.data_gatherers = dict()
        self.out_path = out_path
        for collector_class, processors_class in data_gatherers.items():
            collector = collector_class()
            self.data_gatherers[collector] = list()
            for processor_class in processors_class:
                self.data_gatherers[collector].append(processor_class())

    def start_session(self):
        print(f"start session {self.session_name}...")
        self.session_start_time = time.time()
        for collector in self.data_gatherers:
            collector.start()
        time.sleep(self.session_duration)
        all_data = list()
        for collector in self.data_gatherers:
            all_data.append(collector.stop_collect())
        for collector in self.data_gatherers:
            collector.join()
            del collector
        for i, processors in enumerate(self.data_gatherers.values()):
            for processor in processors:
                processor.set_arguements(all_data[i], self)
                processor.start()
        for processors in self.data_gatherers.values():
            for processor in processors:
                processor.join()
                del processor

        del self.data_gatherers
        gc.collect()

    def set_args(self, front_window_type, window_switches, label):
        self.front_window_type = front_window_type
        self.window_switches = window_switches
        self.label = label

    def save_session(self):
        output_path = self.out_path + "\\session"
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        session_data = {"session": self.session_name,
                        "front_window_type": self.front_window_type,
                        "window_switches": self.window_switches,
                        "label": self.label}
        with open(f"{output_path}\\session_{str(self.session_name)}.json", 'w+') as session_file:
            json.dump(session_data, session_file)



