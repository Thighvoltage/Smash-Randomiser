import tkinter as tk
from winsound import PlaySound, SND_FILENAME, SND_LOOP, SND_ASYNC


class App:

    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack()
        self.button = tk.Button(frame, text='play', command=self.play_sound)
        self.button.pack(side=tk.LEFT)
        self.button2 = tk.Button(frame, text='stop', command=self.stop_sound)
        self.button2.pack(side=tk.LEFT)

    def play_sound(self):
        PlaySound('77-Byleth.wav', SND_FILENAME|SND_LOOP|SND_ASYNC)

    def stop_sound(self):
        PlaySound(None, SND_FILENAME)

root = tk.Tk()
app = App(root)
root.mainloop()
