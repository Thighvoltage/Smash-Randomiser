from tkinter import *
from PIL import Image, ImageTk

root = Tk()

image = Image.open("D:\Pictures\Memes\\69 Reddit Karma.PNG")
photo = ImageTk.PhotoImage(image)


def toggle():

    if toggle_btn.config('relief')[-1] == 'sunken':
        toggle_btn.config(relief="raised")
    else:
        toggle_btn.config(relief="sunken")

toggle_btn = Button(text="Toggle", relief="raised", command = toggle, fg='red',image=photo)
toggle_btn.pack(pady=5)


root.mainloop()
