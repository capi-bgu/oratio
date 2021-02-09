from abc import ABC, abstractmethod

class LabelMethod(ABC):
    def __init__(self):
        self.label = -1
        self.name = "ABSTRACT"

    @abstractmethod
    def get_label(self):
        return {self.name: self.label}
