from tkinter import *
from PIL import Image, ImageTk
import os
import os.path

root = Tk()

image = Image.open(os.getcwd()+"\\Character Icons\\"+"1-Mario.png")
photo = ImageTk.PhotoImage(image)


def toggle():

    if toggle_btn.config('relief')[-1] == 'sunken':
        toggle_btn.config(relief="raised")
    else:
        toggle_btn.config(relief="sunken")

toggle_btn = Button(text="Toggle", relief="raised", command = toggle, fg='red',image=photo)
toggle_btn.pack(pady=5)


root.mainloop()
