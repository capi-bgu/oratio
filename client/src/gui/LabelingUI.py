import tkinter as tk
from abc import ABC, abstractmethod

class LabelingUI(ABC):
    def __init__(self):
        self.label = -1
        self.name = "ABSTRACT"
        self.root = tk.Tk()
        self.root.resizable(0, 0)
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.root.wm_attributes("-topmost", True)

    @abstractmethod
    def exit(self):
        self.root.destroy()
