import os
import pathlib
import tkinter as tk
from PIL import ImageTk, Image
from src.gui.LabelingUI import LabelingUI


class VadSamLabelingUI(LabelingUI):
    def __init__(self):
        super().__init__()
        self.name = "VAD"
        self.valance = 0
        self.arousal = 0
        self.dominance = 0

        curr_dir = pathlib.Path(__file__).parent.absolute()
        self.resources_path = os.path.join(curr_dir, 'resources')

        tk.Label(self.root, text="Valance:", font=(None, 11), justify=tk.CENTER).pack()
        self.valance_sam = Image.open(rf"{self.resources_path}\SAM-V-9.png")
        self.valance_sam = ImageTk.PhotoImage(self.valance_sam)
        label = tk.Label(self.root, image=self.valance_sam)
        label.pack()
        self.valance_scale = tk.Scale(self.root, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, length=1225, showvalue=False)
        self.valance_scale.pack()

        tk.Label(self.root, text="Arousal:", font=(None, 11), justify=tk.CENTER).pack()
        self.arousal_sam = Image.open(rf"{self.resources_path}\SAM-A-9.png")
        self.arousal_sam = ImageTk.PhotoImage(self.arousal_sam)
        label = tk.Label(self.root, image=self.arousal_sam)
        label.pack()
        self.arousal_scale = tk.Scale(self.root, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, length=1225, showvalue=False)
        self.arousal_scale.pack()

        tk.Label(self.root, text="Dominance:", font=(None, 11), justify=tk.CENTER).pack()
        self.dominance_sam = Image.open(rf"{self.resources_path}\SAM-D-9.png")
        self.dominance_sam = ImageTk.PhotoImage(self.dominance_sam)
        label = tk.Label(self.root, image=self.dominance_sam)
        label.pack()
        self.dominance_scale = tk.Scale(self.root, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, length=1225, showvalue=False)
        self.dominance_scale.pack()

        tk.Button(self.root, text="OK", command=self.exit, width=50).pack()
        tk.mainloop()

    def exit(self):
        self.valance = self.valance_scale.get()
        self.arousal = self.arousal_scale.get()
        self.dominance = self.dominance_scale.get()
        self.label = {"Valance": self.valance,
                      "Arousal": self.arousal, 
                      "Dominance": self.dominance}
        super().exit()


if __name__ == '__main__':
    vad = VadSamLabelingUI()
    print(vad.label)

