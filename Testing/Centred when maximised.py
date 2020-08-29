import tkinter as tk

class Example1(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Hello, example1")
        self.label.place(relx=.5, rely=.5, anchor="c")

class Example2(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Hello, example2")
        self.label.grid(row=1, column=1, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    top = tk.Toplevel()
    Example1(root).pack(fill="both", expand=True)
    Example2(top).pack(fill="both", expand=True)

    root.geometry("300x300+100+100")
    top.geometry("300x300+450+100")

    root.mainloop()
