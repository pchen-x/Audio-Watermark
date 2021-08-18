# -*- coding: utf-8 -*-

import soundfile as sf  # To read the samples in our sound file
from PIL import Image  # To create an image
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as tkMessageBox


# Pop up page for GUI
def chooseFile(a):
    global picLoc
    global soundLoc
    # Files are chosen
    if (a == 0):
        tkMessageBox.showinfo("SneakyBits", "Make sure the file is a .png or .jpg format")
        searching = True
        while (searching):
            picLoc = filedialog.askopenfilename()
            picFormatSuffix = picLoc[len(picLoc) - 3:len(picLoc)]
            picFormatSuffix = picFormatSuffix.lower()
            if (picFormatSuffix != "png" and picFormatSuffix != "jpg" and picFormatSuffix != ""):
                tkMessageBox.showwarning("Error", "Has to be .png or .jpg format")
            else:
                searching = False
    if (picLoc != ""):
        tkMessageBox.showinfo("SneakyBits", "Image Selected!")
    elif (a == 1):
        tkMessageBox.showinfo("SneakyBits", "Make sure the file is a .wav format")
        searching = True
        while (searching):
            soundLoc = filedialog.askopenfilename()
            soundFormatSuffix = soundLoc[len(soundLoc) - 3:len(soundLoc)]
            soundFormatSuffix = soundFormatSuffix.lower()
            if (soundFormatSuffix != "wav" and soundFormatSuffix != ""):
                tkMessageBox.showwarning("Error", "Has to be .wav format")
            else:
                searching = False
    if (soundLoc != ""):
        tkMessageBox.showinfo("SneakyBits", "Sound Selected!")


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


# Hide picture page
class HidePicture(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        button1 = tk.Button(self, text="Choose Picture to Hide", command=lambda: chooseFile(0))
        button2 = tk.Button(self, text="Choose Audio to Hide In", command=lambda: chooseFile(1))
        button3 = tk.Button(self, text="Go", command=lambda: setMusic(picLoc, soundLoc))
        button1.pack(side="top", fill="both", expand=True)
        button2.pack(side="top", fill="both", expand=True)
        button3.pack(side="top", fill="both", expand=True)


# Extraction page
class ExtractPicture(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        button1 = tk.Button(self, text="Choose Sound File", command=lambda: chooseFile(1))
        button2 = tk.Button(self, text="Go", command=lambda: newImage(picLoc, soundLoc))
        button1.pack(side="top", fill="both", expand=True)
        button2.pack(side="top", fill="both", expand=True)


# Framework for pages
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = HidePicture(self)
        p2 = ExtractPicture(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Hide a picture", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Extract a picture", command=p2.lift)

        b1.pack(side="left", fill="x", expand=True)
        b2.pack(side="left", fill="x", expand=True)

        p1.show()


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Sneaky Bits")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()

# End of UI
