import gc
from src.Session import Session

class Core:
    def __init__(self, data_gatherers, out_path, num_sessions, session_duration, session_data_handlers,
                 labeling_methods, database_managers, ask_freq=2, sessions_passed=0):
        """

        :param data_gatherers: dictionary for relating collectors to all it's processors,
            and each processor to all it's handlers.
            in the format: {Collector: {Processor: [DataHandler]}}
        :param out_path: path where we want to save the data. str
        :param num_sessions: how many sessions we want to collect. int
        :param session_duration: number of seconds for session. float
        :param session_data_handlers: list of data handlers for session data
        :param labeling_methods: list of labeling ui methods classes. list
        :param database_managers: list of DatabaseManagers that creating the database.
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

        self.database_managers = database_managers
        for database_manager in self.database_managers:
            database_manager.create_database()
        self.session_data_handlers = session_data_handlers
        for session_data_handler in self.session_data_handlers:
            session_data_handler.create_data_holder()
        for processor_handlers_dict in data_gatherers.values():
            for handlers_list in processor_handlers_dict.values():
                for handler in handlers_list:
                    handler.create_data_holder()

    def run(self):
        label = -1
        while self.sessions_passed < self.num_sessions and self.running:
            if self.sessions_passed % self.ask_freq == 0:
                label = self.ask_for_label()
            curr_session = Session(self.sessions_passed, self.session_duration, self.data_gatherers, self.out_path)
            curr_session.start_session()
            curr_session.set_args(-1, -1, label)
            for session_data_handler in self.session_data_handlers:
                session_data_handler.save(curr_session)
            self.sessions_passed += 1
            del curr_session
            gc.collect()

    def ask_for_label(self):
        label = dict()
        for method in self.labeling_methods:
            m = method()
            label[m.name] = m.label
        return label
