import tkinter as tk
from src.gui.LabelingUI import LabelingUI


class VadSamRadioLabelingUI(LabelingUI):
    def __init__(self):
        super().__init__()
        self.valance = tk.IntVar()
        self.arousal = tk.IntVar()
        self.dominance = tk.IntVar()
        feelings = {"no answer": 0,
                    "sad": 1,
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
                           variable=self.valance,
                           value=val).pack(anchor=tk.W)
        for txt, val in feelings.items():
            tk.Radiobutton(self.root,
                           text=txt,
                           padx=20,
                           variable=self.arousal,
                           value=val).pack(anchor=tk.W)
        for txt, val in feelings.items():
            tk.Radiobutton(self.root,
                           text=txt,
                           padx=20,
                           variable=self.dominance,
                           value=val).pack(anchor=tk.W)
        tk.Button(self.root, text="OK", command=self.exit).pack(anchor=tk.W)
        tk.mainloop()

    def exit(self):
        self.label = (self.valance.get(), self.arousal.get(), self.dominance.get())
        super().exit()


if __name__ == '__main__':
    categorical = VadSamRadioLabelingUI()
    print(categorical.label)
