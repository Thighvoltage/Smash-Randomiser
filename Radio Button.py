from tkinter import *

class App:
    def __init__(self, root):
        self.root = root
        self.v = IntVar()
        self.number = 5 #change me to get more buttons
        self.buttons = []
        for i in range(self.number):
            self.buttons.append(Radiobutton(self.root, text="Change!", bg="white", activebackground="lightblue", selectcolor="lightblue", variable=self.v, indicatoron=0, value=i))
            self.buttons[i].pack()

root = Tk()
App(root)
root.mainloop()
