import os
import time
import pathlib
import tkinter as tk
from PIL import ImageTk, Image
from src.labeling.labeling_method.tk_labeling.TkLabelMethod import TkLabelMethod


class VadSamRadioLabelingUI(TkLabelMethod):
    def __init__(self):
        super().__init__()
        self.name = "VAD"

        src_dir = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
        self.resources_path = os.path.join(src_dir, 'resources')


    def get_label(self):
        super().get_label()
        self.root.title('How do you feel?')
        self.valance = tk.IntVar()
        self.arousal = tk.IntVar()
        self.dominance = tk.IntVar()

        self.image_list = []

        self.__build_block("Valance", self.valance, 0)
        self.__build_block("Arousal", self.arousal, 1)
        self.__build_block("Dominance", self.dominance, 2)

        tk.Button(self.root, text="OK", command=self.exit).grid(row=9, column=4)

        tk.mainloop()
        return super(TkLabelMethod, self).get_label()

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
            img_path = os.path.join(self.resources_path, name, f"{name}{i}.png")
            img = Image.open(img_path)
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
        self.label = {"Valance": self.valance.get(),
                      "Arousal": self.arousal.get(),
                      "Dominance": self.dominance.get()}
        super().exit()


if __name__ == '__main__':
    labeler = VadSamRadioLabelingUI()
    print(labeler.get_label())
    time.sleep(3)
    print(labeler.get_label())
