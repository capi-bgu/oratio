from tkinter import *


class Categorical_ui:
    def __init__(self):  # create popup question about user's feeling, active only in Learning Mode.
        self.root = Tk()
        self.root.resizable(0, 0)
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.root.wm_attributes("-topmost", True)
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
            # different styles to show the options
            Radiobutton(self.root,
                        text=txt,
                        padx=20,
                        variable=self.result,
                        value=val).pack(anchor=W)
        Button(self.root, text="OK", command=self.exit).pack(anchor=W)
        mainloop()

    def exit(self):  # check to prevent closing before mark an option
        if self.result.get() != 0:
            self.result = self.result.get()
            self.root.destroy()


if __name__ == '__main__':
    categorical = Categorical_ui()
    print(categorical.result)
