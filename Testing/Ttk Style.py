from tkinter import *
from tkinter.ttk import *

root = Tk()

label_style = Style()
label_style.configure("BW.TLabel", foreground="black", background="white")

l1 = Label(text="Test", style="BW.TLabel")
l2 = Label(text="Test", style="BW.TLabel")

l1.grid(row=0, column=0)
l2.grid(row=0, column=1)

icon_style = Style()
icon_style.configure("TMenubutton", background="gray15",
    relief=FLAT, borderwidth=-1, activebackground="gray15", foreground="white")

'''icon_style.map("TMenubutton",
    foreground=[('pressed', 'white'), ('active', 'white')],
    background=[('pressed', '!disabled', 'black'), ('active', 'black')]
    )'''

style = Style()
style.layout("TMenubutton", [
   ("Menubutton.background", None),
   ("Menubutton.button", {"children":
       [("Menubutton.focus", {"children":
           [("Menubutton.padding", {"children":
               [("Menubutton.label", {"side": "left", "expand": 1})]
           })]
       })]
   }),
])


poo = Button(text="Button", style="TMenubutton")
poo.grid(row=0, column=2)

root.mainloop()
