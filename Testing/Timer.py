import tkinter as tk
import time

class A:
    def __init__(self, master):
        self.button = tk.Button(master, text='click me', command=self.f)
        self.button.grid(row=0, column=0)
        self.remaining = 10

    def f(self):
        #self.remaining gets updated here
        #it is amount of task yet to be done
        #like a 'count down'
        if self.remaining > 0:
            self.button.configure(text='timer {}'.format(self.remaining))
            self.button.after(1000, self.f)
            self.remaining -= 1

root = tk.Tk()
A(root)
root.mainloop()
