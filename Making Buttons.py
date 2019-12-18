from tkinter import *
import os
import os.path

root = Tk()
image = PhotoImage(file=os.getcwd()+"\\Character Icons\\1-Mario.png")
for _ in range(5):
    Button(root, image=image, borderwidth=0, relief=SUNKEN).pack()
root.mainloop()
