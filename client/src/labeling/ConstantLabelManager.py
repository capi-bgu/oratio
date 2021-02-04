from src.labeling.AbsLabelManager import AbsLabelManager


class ConstantLabelManager(AbsLabelManager):
    def __init__(self, labeling_methods, ask_freq):
        super().__init__(labeling_methods)
        self.ask_freq = ask_freq

    def get_label(self, session, now=False):
        if session.id % self.ask_freq == 0 or now:
            self.label = self.__ask_for_label()
        return self.label

    def __ask_for_label(self):
        label = dict()
        for method in self.labeling_methods:
            m = method()
            label[m.name] = m.label
        return label
