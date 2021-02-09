from abc import ABC, abstractmethod

class LabelManager(ABC):
    def __init__(self, labeling_methods):
        self.label = None
        self.labeling_methods = labeling_methods

    @abstractmethod
    def get_label(self, session, now=False):
        pass

    def ask_for_label(self):
        label = dict()
        for method in self.labeling_methods:
            label.update(method.get_label())
        return label
