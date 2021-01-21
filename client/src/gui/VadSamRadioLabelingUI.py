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

        self.image_list = []

        self.__build_block("Valance", self.valance, 0)
        self.__build_block("Arousal", self.arousal, 1)
        self.__build_block("Dominance", self.dominance, 2)

        tk.Button(self.root, text="OK", command=self.exit).grid(row=9, column=4)
        tk.mainloop()

    def __build_block(self, name, out, block_number):
        row = block_number * 3
        # First Row
        tk.Label(self.root,
                 text=f"{name}:",
                 font=(None, 11),
                 justify=tk.CENTER).grid(row=row, column=4)

        # Second Row
        row += 1
        self.image_list.append(list())  # this list is for the pictures to stay in the memory
        for i in range(9):
            canvas2 = tk.Canvas(self.root, width=110, height=110)
            img = Image.open(f"resources/{name}/{name}{i}.png")
            img = img.resize((90, 90), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            canvas2.create_image(50, 50, anchor=tk.CENTER, image=img)
            canvas2.grid(row=row, column=i)
            self.image_list[block_number].append(img)

        # Third Row
        row += 1
        for i in range(9):
            tk.Radiobutton(self.root,
                           variable=out,
                           value=i - 4).grid(row=row, column=i)

    def exit(self):
        self.label = (self.valance.get(), self.arousal.get(), self.dominance.get())
        super().exit()


if __name__ == '__main__':
    categorical = VadSamRadioLabelingUI()
    print(categorical.label)
