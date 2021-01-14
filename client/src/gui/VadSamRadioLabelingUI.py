import tkinter as tk
from src.gui.LabelingUI import LabelingUI


class VadSamRadioLabelingUI(LabelingUI):
    def __init__(self):
        super().__init__()
        self.valance = tk.IntVar()
        feelings = {"sad": 1,
                    "anger": 2,
                    "fear": 3,
                    "happy": 4,
                    "surprised": 5,
                    'stressed': 6}
        tk.Label(self.root,
                 text="How are you feeling?",
                 justify=tk.LEFT,
                 padx=20).pack()
        for txt, val in feelings.items():
            tk.Radiobutton(self.root,
                           text=txt,
                           padx=20,
                           variable=self.result,
                           value=val).pack(anchor=tk.W)
        tk.Button(self.root, text="OK", command=self.exit).pack(anchor=tk.W)
        tk.mainloop()

    def exit(self):
        if self.result.get() != 0:
            self.label = self.result.get()
            super().exit()


if __name__ == '__main__':
    categorical = VadSamRadioLabelingUI()
    print(categorical.label)
