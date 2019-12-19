from tkinter import *
from PIL import Image, ImageTk
import os
import os.path

characters = []
DARKNESS_LEVEL = 0.3

class Character:
    def __init__(self, num, name, image, photo, icon, portrait, display, dark):
        self.num = num
        self.name = name
        self.image = image
        self.photo = photo
        self.icon = icon
        self.portrait = portrait
        self.display = display
        self.dark = dark

class GUI:
    def __init__(self, master):

        COLOUR_BG = "gray15"

        self.master = master

        self.frame_characters = Frame(master, bg = COLOUR_BG)
        self.frame_characters.grid(row = 0, column = 0, sticky = 'nesw')

        #self.master.grid_columnconfigure(0, weight = 1)
        #self.master.grid_rowconfigure(0, weight = 1)

        for i in range(len(characters)):
            characters[i].icon = Button(self.frame_characters,
                                 image = characters[i].photo, relief = FLAT,
                                 borderwidth = -1, bg = COLOUR_BG,
                                 activebackground = COLOUR_BG, command =
                                 lambda i=i: self.select(i))
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
                characters[i].icon.grid(row = 5, column = i - 60)
            else:
                characters[i].icon.grid(row = 6, column = i -
                    round((72 - (12 - (len(characters) - 72)) / 2)))
                if (len(characters) - 72) % 2 != 0:
                    characters[i].icon.grid(columnspan = 2, sticky = N)

        self.frame_portrait = Frame(master, bg = COLOUR_BG)
        self.frame_portrait.grid(row = 1, column = 0, sticky = NW)

        for i in range(len(characters)):
            characters[i].display = Label(self.frame_portrait,
                                    image = characters[i].portrait,
                                    borderwidth = -1, bg = COLOUR_BG,
                                    activebackground = COLOUR_BG)

        characters[22].display.grid(row = 0, column = 0)

    def select(self, i):
        if characters[i].dark == FALSE:
            characters[i].photo = ImageTk.PhotoImage(characters[i].image.point(lambda p: p * DARKNESS_LEVEL))
            characters[i].icon.configure(image = characters[i].photo)
            characters[i].dark = TRUE

        elif characters[i].dark == TRUE:
            characters[i].photo = ImageTk.PhotoImage(characters[i].image)
            characters[i].icon.configure(image = characters[i].photo)
            characters[i].dark = FALSE

def characters_get():
    character_icons = [name for name in os.listdir(os.getcwd()+"\\Character Icons")]
    character_portraits = [name for name in os.listdir(os.getcwd()+"\\Character Portraits")]

    index = 0
    for name in os.listdir(os.getcwd()+"\\Character Icons"):
        icon_image = Image.open(os.getcwd()+"\\Character Icons\\"+str(name))
        icon_photo = ImageTk.PhotoImage(icon_image)
        portrait_image = Image.open(os.getcwd()+"\\Character Portraits\\"+str(name))
        portrait_photo = ImageTk.PhotoImage(portrait_image)

        temp = character_icons[index].split("-")
        temp[0] = int(temp[0])
        temp[1] = temp[1].replace(".png", "")
        characters.append(Character(temp[0], temp[1], icon_image, icon_photo, 1, portrait_photo, 1, FALSE))
        index += 1

    characters.sort(key = lambda x: x.num)
'''
    for index in range(len(characters)):
        print(index, characters[index].num, characters[index].name)
'''
def main():
    """Runs the GUI and assigns it a name
    """

    global root
    root = Tk()
    root.configure(bg = "gray15")
    characters_get()
    root.title("Smash Randomiser")
    app = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    """Runs main() if this program hasn't been imported
    """
    main()
