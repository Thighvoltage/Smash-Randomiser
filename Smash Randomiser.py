from tkinter import *
from PIL import Image, ImageTk
import os
import os.path

class Character:
    def __init__(self, num, name, image, icon):
        self.num = num
        self.name = name
        self.image = image
        self.icon = icon

class GUI:
    def __init__(self, master):
        self.master = master

        self.frame_characters = Frame(master, bg = "gray15")
        self.frame_characters.grid(row = 0, column = 0)

        for i in range(len(characters)):
            characters[i].icon = Button(self.frame_characters,
                                 image = characters[i].image,relief = FLAT,
                                 borderwidth = -1, bg = "gray15",
                                 activebackground = "gray15", command =
                                 lambda i=i: self.select(i + 1))
            if i < 12:
                characters[i].icon.grid(row = 0, column = i)
            elif i < 24:
                characters[i].icon.grid(row = 1, column = i - 12)
            elif i < 36:
                characters[i].icon.grid(row = 2, column = i - 24)
            elif i < 48:
                characters[i].icon.grid(row = 3, column = i - 36)
            elif i < 60:
                characters[i].icon.grid(row = 4, column = i - 48)
            elif i < 72:
                characters[i].icon.grid(row = 4, column = i - 60)
            else:
                characters[i].icon.grid(row = 5, column = i - round((72 - (12 - (len(characters) - 72)) / 2)))
                if (len(characters) - 72) % 2 != 0:
                    characters[i].icon.grid(columnspan = 2, sticky = N)

    def select(self, i):
        print(i)

characters = []

def characters_get():
    characters_raw = [name for name in os.listdir(os.getcwd()+"\\Character Icons")]

    index = 0
    for name in os.listdir(os.getcwd()+"\\Character Icons"):
        image = ImageTk.PhotoImage(Image.open(os.getcwd()+"\\Character Icons\\"+str(name)))
        temp = characters_raw[index].split("-")
        temp[0] = int(temp[0])
        temp[1] = temp[1].replace(".png", "")
        characters.append(Character(temp[0], temp[1], image, 1))
        index += 1

    characters.sort(key = lambda x: x.num)

def main():
    """Runs the GUI and assigns it a name
    """

    global root
    root = Tk()
    characters_get()
    root.title("Smash Randomiser")
    app = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    """Runs main() if this program hasn't been imported
    """
    main()
