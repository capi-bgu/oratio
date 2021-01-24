import os
import gc
import pathlib
from src.Session import Session
from src.gui.VadSamLabelongUI import VadSamLabelingUI
from src.gui.VadSamRadioLabelingUI import VadSamRadioLabelingUI
from src.gui.CategoricalLabelingUI import CategoricalLabelingUI
from src.collection.MouseCollector import MouseCollector
from src.processing.MouseProcessor import MouseProcessor
from src.collection.CameraCollector import CameraCollector
from src.processing.CameraProcessor import CameraProcessor
from src.collection.KeyboardCollector import KeyboardCollector
from src.processing.KeyboardProcessor import KeyboardProcessor

class Core:
    def __init__(self, data_gatherers, out_path, num_sessions, session_duration, session_data_handlers,
                 labeling_methods, database_managers, ask_freq=2, sessions_passed=0):
        """

        :param data_gatherers: dictionary of collectors classes and the list of all related processors classes
            in the format: {CollectorClass: ([*(ProcessorClass, DataHandlerClass)]}. dictionary
        :param out_path: path where we want to save the data. str
        :param num_sessions: how many sessions we want to collect. int
        :param session_duration: number of seconds for session. float
        :param session_data_handlers: list of data handlers classes for session data
        :param labeling_methods: list of labeling ui methods. list
        :param database_managers: list of managers that creating the database- in order with DataHandlerClasses.
            list of Database Managers classes
        :param ask_freq: how many sessions to wait between each labeling query. int
        :param sessions_passed: how many sessions already passed. int
        """

        self.num_sessions = num_sessions
        self.sessions_passed = sessions_passed
        self.session_duration = session_duration
        self.data_gatherers = data_gatherers
        self.out_path = out_path
        self.running = True
        self.ask_freq = ask_freq
        self.labeling_methods = labeling_methods

        self.database_managers = [db_manager().create_database() for db_manager in database_managers]
        self.session_data_handlers = [session_data_handler() for session_data_handler in session_data_handlers]

    def run(self):
        label = -1
        while self.sessions_passed < self.num_sessions and self.running:
            if self.sessions_passed % self.ask_freq == 0:
                label = self.ask_for_label()
            curr_session = Session(self.sessions_passed, self.session_duration, self.data_gatherers, self.out_path)
            curr_session.start_session()
            self.sessions_passed += 1
            curr_session.set_args(-1, -1, label)
            for session_data_handler in self.session_data_handlers:
                session_data_handler.save(curr_session)
            del curr_session
            gc.collect()

    def ask_for_label(self):
        label = dict()
        for method in self.labeling_methods:
            m = method()
            label[m.name] = m.label
        return label


if __name__ == '__main__':
    test_dir = pathlib.Path(__file__).parent.parent.absolute()

    if not os.path.isdir("../test_output"):
        os.mkdir("../test_output")

    out_path = os.path.join(test_dir, 'test_output')
    data_gatherers = {KeyboardCollector: [KeyboardProcessor],
                      CameraCollector: [CameraProcessor],
                      MouseCollector: [MouseProcessor]}
    label_methods = [CategoricalLabelingUI, VadSamLabelingUI, VadSamRadioLabelingUI]
    core = Core(data_gatherers, out_path, num_sessions=4, session_duration=5, labeling_methods=label_methods)
    core.run()
