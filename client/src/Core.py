import os
import gc
import pathlib
from src.Session import Session
from src.gui.SAM_ui import SAM_ui
from src.gui.Categorical_ui import Categorical_ui
from src.collection.MouseCollector import MouseCollector
from src.processing.MouseProcessor import MouseProcessor
from src.collection.CameraCollector import CameraCollector
from src.processing.CameraProcessor import CameraProcessor
from src.collection.KeyboardCollector import KeyboardCollector
from src.processing.KeyboardProcessor import KeyboardProcessor

class Core:
    def __init__(self, data_gatherers, out_path, num_sessions, session_duration, vad_labels=True,
                 categorical_labels=True, ask_freq=2, sessions_passed=0):
        """

        :param data_gatherers: dictionary of collectors classes and the list of all related processors classes
            in the format: {CollectorClass: [*ProcessorClass]}
        """

        self.num_sessions = num_sessions
        self.sessions_passed = sessions_passed
        self.session_duration = session_duration
        self.data_gatherers = data_gatherers
        self.out_path = out_path
        self.curr_session = None
        self.running = True
        self.ask_freq = ask_freq
        self.vad_labels = vad_labels
        self.categorical_labels = categorical_labels

    def run(self):
        label = -1
        while self.sessions_passed < self.num_sessions and self.running:
            if self.sessions_passed % self.ask_freq == 0:
                label = self.ask_for_label()
            self.curr_session = Session(self.sessions_passed, self.session_duration, self.data_gatherers, self.out_path)
            self.curr_session.start_session()
            self.sessions_passed += 1
            self.curr_session.set_args(-1, -1, label)
            self.curr_session.save_session()
            del self.curr_session
            gc.collect()

    def ask_for_label(self):
        label = list()
        if self.categorical_labels:
            label.append(Categorical_ui().result)
        if self.vad_labels:
            label.append(SAM_ui().result)
        return label


if __name__ == '__main__':
    test_dir = pathlib.Path(__file__).parent.parent.absolute()

    if not os.path.isdir("../test_output"):
        os.mkdir("../test_output")

    out_path = os.path.join(test_dir, 'test_output')
    data_gatherers = {KeyboardCollector: [KeyboardProcessor],
                      CameraCollector: [CameraProcessor],
                      MouseCollector: [MouseProcessor]}
    core = Core(data_gatherers, out_path, num_sessions=4, session_duration=5)
    core.run()