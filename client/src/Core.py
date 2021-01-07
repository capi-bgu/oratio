import os
import gc
import pathlib
from src.Session import Session
from src.collection.MouseCollector import MouseCollector
from src.processing.MouseProcessor import MouseProcessor
from src.collection.CameraCollector import CameraCollector
from src.processing.CameraProcessor import CameraProcessor
from src.collection.KeyboardCollector import KeyboardCollector
from src.processing.KeyboardProcessor import KeyboardProcessor

class Core:
    def __init__(self, data_gatherers, out_path, num_sessions, session_duration, sessions_passed=0):
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

    def run(self):
        while self.sessions_passed < self.num_sessions and self.running:
            self.curr_session = Session(self.sessions_passed, self.session_duration, self.data_gatherers, self.out_path)
            self.curr_session.start_session()
            self.sessions_passed += 1
            del self.curr_session
            gc.collect()


if __name__ == '__main__':
    test_dir = pathlib.Path(__file__).parent.parent.absolute()

    if not os.path.isdir("../test_output"):
        os.mkdir("../test_output")

    out_path = os.path.join(test_dir, 'test_output')
    data_gatherers = {KeyboardCollector: [KeyboardProcessor],
                      CameraCollector: [CameraProcessor],
                      MouseCollector: [MouseProcessor]}
    core = Core(data_gatherers, out_path, num_sessions=3, session_duration=5)
    core.run()

