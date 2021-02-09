import gc
from src.Session import Session


class Core:
    def __init__(self, data_gatherers, out_path, num_sessions, session_duration,
                 database_managers, label_manager):
        """

        :param data_gatherers: dictionary for relating collectors to all it's processors,
            and each processor to all it's handlers.
            in the format: {Collector: {Processor: [DataHandler]}}
        :param out_path: path where we want to save the data. str
        :param num_sessions: how many sessions we want to collect. int
        :param session_duration: number of seconds for session. float
        :param database_managers: list of DatabaseManagers that creating the database.
        :param label_manager: Label manager object. decide when to pop up question for new label to the user.
        :param sessions_passed: how many sessions already passed. int
        """

        self.session_duration = session_duration
        self.data_gatherers = data_gatherers
        self.label_manager = label_manager
        self.num_sessions = num_sessions
        self.out_path = out_path
        self.running = False

        self.database_managers = database_managers
        for database_manager in self.database_managers:
            database_manager.create_data_holder()

        for processor_handlers_dict in data_gatherers.values():
            for handlers_list in processor_handlers_dict.values():
                for handler in handlers_list:
                    handler.create_data_holder()

        self.sessions_passed = len(self.database_managers[0])

    def run(self):
        first_session = True
        self.running = True
        while self.sessions_passed < self.num_sessions and self.running:
            curr_session = Session(self.sessions_passed, self.session_duration, self.data_gatherers, self.out_path)
            curr_session.start_session()
            label = self.label_manager.get_label(curr_session, first_session)
            curr_session.set_label(label)
            for session_data_handler in self.database_managers:
                session_data_handler.save_session(curr_session)
            self.sessions_passed += 1
            first_session = False
            del curr_session
            gc.collect()

    def stop(self):
        self.running = False
