import pathlib
import json
import numpy as np
from itertools import groupby
from src.processing.DataProcessor import DataProcessor


class SessionMetaProcessor(DataProcessor):
    def __init__(self):
        super().__init__()
        processing_dir = pathlib.Path(__file__).parent.absolute()
        with open(f"{processing_dir}/task_keywords.json") as keywords_file:
            self.task_keywords = json.load(keywords_file)

    def process_data(self, data, session):
        self.__init_features()

        data = [f"{window_name.lower()} :: {process_name.lower()}" for window_name, process_name in data]
        names = np.array(data)
        unique_names, name_counts = np.unique(names, return_counts=True)
        self.features["dominate_window"] = unique_names[np.argmax(name_counts)].split('::')[0][:-1]
        self.features["window_switches"] = len(list(groupby(names))) - 1
        self.features["window_count"] = len(unique_names)

        tasks = map(self.__name_to_task, data)
        tasks = [task_group[0] for task_group in groupby(tasks)]
        unique_tasks, task_counts = np.unique(tasks, return_counts=True)
        self.features["dominate_task"] = unique_tasks[np.argmax(task_counts)]
        self.features["task_switches"] = len(tasks)
        self.features["task_count"] = len(unique_tasks)

        return self.features

    def __name_to_task(self, window_name: str):
        for task in self.task_keywords.keys():
            if any([keyword in window_name for keyword in self.task_keywords[task]]):
                return task
        return "Unknown"

    def __init_features(self):
        self.features = {
            "dominate_window": "",
            "dominate_task": "",
            "window_switches": 0,
            "task_switches": 0,
            "window_count": 0,
            "task_count": 0
        }
