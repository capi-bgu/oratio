from tkinter import *
from PIL import ImageTk, Image
from src.gui.LabelingUI import LabelingUI


class VadSamLabelingUI(LabelingUI):
    def __init__(self):
        super().__init__()
        self.valance = 0
        self.arousal = 0
        self.dominance = 0
        self.result = 0

        self.root.geometry('1300x550')

        self.valance_sam = Image.open(r"C:\Users\Hod\Desktop\bgu\Year4\project\CAPI_2.0\capi\client\src\gui\resources\SAM-V-9.png")
        self.valance_sam = ImageTk.PhotoImage(self.valance_sam)
        label = Label(self.root, image=self.valance_sam)
        label.pack()
        self.valance_scale = Scale(self.root, from_=-5, to=5, resolution=0.1, orient=HORIZONTAL, length=1225, showvalue=False)
        self.valance_scale.pack()

        self.arousal_sam = Image.open(r"C:\Users\Hod\Desktop\bgu\Year4\project\CAPI_2.0\capi\client\src\gui\resources\SAM-A-9.png")
        self.arousal_sam = ImageTk.PhotoImage(self.arousal_sam)
        label = Label(self.root, image=self.arousal_sam)
        label.pack()
        self.arousal_scale = Scale(self.root, from_=-5, to=5, resolution=0.1, orient=HORIZONTAL, length=1225, showvalue=False)
        self.arousal_scale.pack()

        self.dominance_sam = Image.open(r"C:\Users\Hod\Desktop\bgu\Year4\project\CAPI_2.0\capi\client\src\gui\resources\SAM-D-9.png")
        self.dominance_sam = ImageTk.PhotoImage(self.dominance_sam)
        label = Label(self.root, image=self.dominance_sam)
        label.pack()
        self.dominance_scale = Scale(self.root, from_=-5, to=5, resolution=0.1, orient=HORIZONTAL, length=1225, showvalue=False)
        self.dominance_scale.pack()

        Button(self.root, text="OK", command=self.exit, width=50).pack()
        mainloop()

    def exit(self):
        self.valance = self.valance_scale.get()
        self.arousal = self.arousal_scale.get()
        self.dominance = self.dominance_scale.get()
        self.label = [self.valance, self.arousal, self.dominance]
        super().exit()


if __name__ == '__main__':
    vad = VadSamLabelingUI()
    print(vad.label)

