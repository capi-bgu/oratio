import tkinter as tk
from abc import abstractmethod
from src.labeling.labeling_method.LabelMethod import LabelMethod


class TkLabelMethod(LabelMethod):

    def __init__(self):
        super().__init__()
        self.name = "TK_ABSTRACT"

    @abstractmethod
    def get_label(self):
        self.root = tk.Tk()
        self.root.resizable(0, 0)
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.root.wm_attributes("-topmost", True)

    @abstractmethod
    def exit(self):
        self.root.destroy()
