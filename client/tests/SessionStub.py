import time

class SessionStub:
    def __init__(self, session_id, session_duration, session_start_time):
        self.session_name = session_id
        self.session_duration = session_duration
        self.session_start_time = session_start_time
