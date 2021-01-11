from tkinter import *
from PIL import ImageTk, Image



class SAM_ui:
    def __init__(self):  # create popup question about user's feeling, active only in Learning Mode.
        self.valance = 0
        self.arousal = 0
        self.dominance = 0
        self.result = 0

        self.master = Tk()
        self.master.geometry('1300x550')
        self.master.wm_attributes("-topmost", True)
        self.master.protocol('WM_DELETE_WINDOW', self.exit)

        self.valance_sam = Image.open(r"C:\Users\Hod\Desktop\bgu\Year4\project\CAPI_2.0\capi\client\src\gui\SAM-V-9.png")
        self.valance_sam = ImageTk.PhotoImage(self.valance_sam)
        label = Label(self.master, image=self.valance_sam)
        label.pack()
        self.valance_scale = Scale(self.master, from_=-5, to=5, resolution=0.1, orient=HORIZONTAL, length=1225, showvalue=FALSE)
        self.valance_scale.pack()

        self.arousal_sam = Image.open(r"C:\Users\Hod\Desktop\bgu\Year4\project\CAPI_2.0\capi\client\src\gui\SAM-A-9.png")
        self.arousal_sam = ImageTk.PhotoImage(self.arousal_sam)
        label = Label(self.master, image=self.arousal_sam)
        label.pack()
        self.arousal_scale = Scale(self.master, from_=-5, to=5, resolution=0.1, orient=HORIZONTAL, length=1225, showvalue=FALSE)
        self.arousal_scale.pack()

        self.dominance_sam = Image.open(r"C:\Users\Hod\Desktop\bgu\Year4\project\CAPI_2.0\capi\client\src\gui\SAM-D-9.png")
        self.dominance_sam = ImageTk.PhotoImage(self.dominance_sam)
        label = Label(self.master, image=self.dominance_sam)
        label.pack()
        self.dominance_scale = Scale(self.master, from_=-5, to=5, resolution=0.1, orient=HORIZONTAL, length=1225, showvalue=FALSE)
        self.dominance_scale.pack()

        Button(self.master, text="OK", command=self.exit, width=50).pack()
        mainloop()

    def exit(self):
        self.valance = self.valance_scale.get()
        self.arousal = self.arousal_scale.get()
        self.dominance = self.dominance_scale.get()
        self.result = [self.valance, self.arousal, self.dominance]
        self.master.destroy()


if __name__ == '__main__':
    vad = SAM_ui()
    print(vad.result)

