import time


class Session:
    def __init__(self, session_id, session_duration, data_gatherers):
        self.session_name = session_id
        self.session_duration = session_duration
        self.session_start_time = time.time()

    def start_session(self):
        pass
