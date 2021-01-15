import tkinter as tk
from src.gui.LabelingUI import LabelingUI
from PIL import ImageTk, Image


class VadSamRadioLabelingUI(LabelingUI):
    def __init__(self):
        super().__init__()
        self.valance = tk.IntVar()
        self.arousal = tk.IntVar()
        self.dominance = tk.IntVar()
        self.root.title('How do you feel?')
        # First Row
        tk.Label(self.root,
                 text="Arousal:",
                 font=(None, 11),
                 justify=tk.CENTER).grid(row=0, column=4)
        # Second Row
        arousal_image_list = []  # this list is for the pictures to stay in the memory
        for i in range(9):
            canvas2 = tk.Canvas(self.root, width=110, height=110)
            img = Image.open("resources/Arousal/Arousal" + str(i) + ".png")
            img = img.resize((90, 90), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            canvas2.create_image(50, 50, anchor=tk.CENTER, image=img)
            canvas2.grid(row=1, column=i)
            arousal_image_list.append(img)
        # Third Row
        for i in range(9):
            tk.Radiobutton(self.root,
                           variable=self.valance,
                           value=i - 4).grid(row=2, column=i)
        # Fourth Row
        tk.Label(self.root,
                 text="Valance:",
                 font=(None, 11),
                 justify=tk.CENTER).grid(row=3, column=4)
        # Fifth Row
        valance_image_list = []  # this list is for the pictures to stay in the memory
        for i in range(9):
            canvas2 = tk.Canvas(self.root, width=110, height=110)
            img = Image.open("resources/Valance/Valance" + str(i) + ".png")
            img = img.resize((90, 90), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            canvas2.create_image(50, 50, anchor=tk.CENTER, image=img)
            canvas2.grid(row=4, column=i)
            valance_image_list.append(img)
        # Sixth Row
        for i in range(9):
            tk.Radiobutton(self.root,
                           variable=self.arousal,
                           value=i - 4).grid(row=5, column=i)
        # Seventh Row
        tk.Label(self.root,
                 text="Dominance:",
                 font=(None, 11),
                 justify=tk.CENTER).grid(row=6, column=4)
        # Eighth Row
        dominance_image_list = []  # this list is for the pictures to stay in the memory
        for i in range(9):
            canvas2 = tk.Canvas(self.root, width=110, height=110)
            img = Image.open("resources/Dominance/Dominance" + str(i) + ".png")
            img = img.resize((90, 90), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            canvas2.create_image(50, 50, anchor=tk.CENTER, image=img)
            canvas2.grid(row=7, column=i)
            dominance_image_list.append(img)
        # Ninth Row
        for i in range(9):
            tk.Radiobutton(self.root,
                           variable=self.dominance,
                           value=i - 4).grid(row=8, column=i)
        # Tenth Row
        tk.Button(self.root, text="OK", command=self.exit).grid(row=9, column=4)
        tk.mainloop()

    def exit(self):
        self.label = (self.valance.get(), self.arousal.get(), self.dominance.get())
        super().exit()


if __name__ == '__main__':
    categorical = VadSamRadioLabelingUI()
    print(categorical.label)
