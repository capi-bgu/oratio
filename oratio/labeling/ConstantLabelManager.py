from oratio.labeling.LabelManager import LabelManager


class ConstantLabelManager(LabelManager):
    def __init__(self, labeling_methods, ask_freq):
        super().__init__(labeling_methods)
        self.ask_freq = ask_freq

    def get_label(self, session, start_session_id):
        sessions_since_start = session.id - start_session_id
        if sessions_since_start % self.ask_freq == 0:
            self.label = self.ask_for_label()
        return self.label


