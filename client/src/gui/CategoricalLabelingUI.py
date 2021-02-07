import logging
from tkinter import *
from src.gui.LabelingUI import LabelingUI


class CategoricalLabelingUI(LabelingUI):
    def __init__(self):
        super().__init__()
        self.name = "Categorical"
        self.result = IntVar()
        feelings = {"sad": 1,
                    "anger": 2,
                    "fear": 3,
                    "happy": 4,
                    "surprised": 5,
                    'stressed': 6}
        Label(self.root,
              text="How are you feeling?",
              justify=LEFT,
              padx=20).pack()
        for txt, val in feelings.items():
            Radiobutton(self.root,
                        text=txt,
                        padx=20,
                        variable=self.result,
                        value=val).pack(anchor=W)
        Button(self.root, text="OK", command=self.exit).pack(anchor=W)
        mainloop()

    def exit(self):  # check to prevent closing before mark an option
        if self.result.get() != 0:
            self.label = self.result.get()
            super().exit()


if __name__ == '__main__':
    categorical = CategoricalLabelingUI()
    print(categorical.label)
