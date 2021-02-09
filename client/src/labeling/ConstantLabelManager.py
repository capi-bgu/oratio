from src.labeling.LabelManager import LabelManager


class ConstantLabelManager(LabelManager):
    def __init__(self, labeling_methods, ask_freq):
        super().__init__(labeling_methods)
        self.ask_freq = ask_freq

    def get_label(self, session, now=False):
        if session.id % self.ask_freq == 0 or now:
            self.label = self.ask_for_label()
        return self.label


