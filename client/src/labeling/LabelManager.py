from abc import ABC, abstractmethod

class LabelManager(ABC):
    def __init__(self, labeling_methods):
        self.label = None
        self.labeling_methods = labeling_methods

    @abstractmethod
    def get_label(self, session, now=False):
        pass
