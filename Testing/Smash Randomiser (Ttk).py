from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import os
import os.path
import random
import time

characters = []
DARKNESS_LEVEL = 0.3
BRIGHTNESS_LEVEL = 1.3

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
        self.BG_COLOUR = "gray15"
        self.BG_COLOUR2 = "gray25"
        self.TEXT_COLOUR = "white"

        self.master = master
        self.master.configure(background="gray15")

        self.init_icon_frame()
        self.init_option_frame()
        #self.init_portrait_frame()


    def init_icon_frame(self):
        """Initialises and fills the icon frame."""
        self.icon_frame = Frame(self.master)
        self.icon_frame.grid(row=0, column=0, columnspan=2, sticky='nesw')
        self.display_icons()


    def display_icons(self):
        """Creates a button for each character and arranges them in order
           in the icon frame.
        """
        LENGTH = 12
        HEIGHT = len(characters) // LENGTH + 1
        FREE_SPACE = (LENGTH - len(characters) % LENGTH)
        LEFT_SPACE = FREE_SPACE // 2
        style = Style()
        style.configure("TMenubutton", background="gray15",
            borderwidth=0, foreground="white", padding=0, font="20")
        style.configure("TButton", background="gray25",
            borderwidth=0, foreground="white", font="20")

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

        style.layout("TButton", [
           ("Menubutton.background", None),
           ("Menubutton.button", {"children":
               [("Menubutton.focus", {"children":
                   [("Menubutton.padding", {"children":
                       [("Menubutton.label", {"side": "left", "expand": 1})]
                   })]
               })]
           }),
        ])

        for i in range(len(characters)):
            characters[i].icon = Button(self.icon_frame,
                                 image=characters[i].photo, command=
                                 lambda i=i: self.select_icon(i), style="TMenubutton")

            if i//LENGTH != HEIGHT-1:
                characters[i].icon.grid(row=i//LENGTH, column=i%LENGTH)
            else:
                characters[i].icon.grid(row=HEIGHT, column=i%LENGTH+LEFT_SPACE)
                if FREE_SPACE % 2 != 0:
                    characters[i].icon.grid(columnspan=2)


    def init_option_frame(self):
        """Initialises and fills the option frame."""
        SELECT_TEXT = "Select a Character"
        ALL_TEXT = "Select All"
        NONE_TEXT = "Select None"

        self.option_frame = Frame(self.master, style="TMenubutton")
        self.option_frame.grid(row=1, column=1, sticky=NW)

        self.select_button = Button(self.option_frame, text=SELECT_TEXT,
                                    command=self.select_character, style="TButton", width=20)

        self.select_button.grid(row=0, column=1, sticky=NW)
        '''
        self.all_button = Button(self.option_frame, text=ALL_TEXT,
                                 command=self.select_all,
                                 fg=self.TEXT_COLOUR, bg=self.BG_COLOUR2,
                                 activebackground=self.BG_COLOUR2,
                                 activeforeground=self.TEXT_COLOUR,
                                 width=10, height=1, font="20")

        self.all_button.grid(row=0, column=0, sticky=NW)

        self.none_button = Button(self.option_frame, text=NONE_TEXT,
                                 command=self.deselect_all,
                                 fg=self.TEXT_COLOUR, bg=self.BG_COLOUR2,
                                 activebackground=self.BG_COLOUR2,
                                 activeforeground=self.TEXT_COLOUR,
                                 width=10, height=1, font="20")

        self.none_button.grid(row=0, column=3, sticky=NW)
        '''

    def select(self, i):
        """Turns an icon bright."""
        characters[i].photo = ImageTk.PhotoImage(characters[i].image)
        characters[i].icon.configure(image=characters[i].photo)
        characters[i].dark = False


    def deselect(self, i):
        """Turns an icon dark."""
        characters[i].photo = ImageTk.PhotoImage(characters[i].image.point(lambda p: p * DARKNESS_LEVEL))
        characters[i].icon.configure(image=characters[i].photo)
        characters[i].dark = True


    def select_all(self):
        """Turns all icons bright."""
        for i in range(len(characters)):
            self.select(i)


    def deselect_all(self):
        """Turns all icons dark."""
        for i in range(len(characters)):
            self.deselect(i)


    def select_icon(self, i):
        """Turns an icon dark if it's bright, or turns an icon bright if it's
           dark.
        """
        if characters[i].dark == True:
            self.select(i)
        else:
            self.deselect(i)


    def init_portrait_frame(self):
        """Initialises the portrait frame."""
        self.portrait_frame = Frame(self.master, bg=self.BG_COLOUR)
        self.portrait_frame.grid(row=1, column=0, sticky=NW)


    def select_character(self):
        pass


def characters_get():
    """Gets the image and name data for each character then creates a class for
       each.
    """
    icon_names = [name for name in os.listdir(os.getcwd()+"\\Character Icons")]
    portrait_names = [name for name in os.listdir(os.getcwd()+"\\Character Portraits")]

    for i, name in enumerate(icon_names):
        image = Image.open(os.getcwd()+"\\Character Icons\\"+str(name))
        photo = ImageTk.PhotoImage(image)
        #portrait_image = Image.open(os.getcwd()+"\\Character Portraits\\"+str(name))
        #portrait_photo = ImageTk.PhotoImage(portrait_image)

        num_and_name = character_num_and_name(icon_names[i])
        characters.append(Character(num_and_name[0], num_and_name[1],
                                    image, photo, 1, 1, 1, False))

    characters.sort(key = lambda x: x.num)

def character_num_and_name(icon_name):
    """Returns [num, name] for """
    num_and_name = icon_name.split("-")
    num_and_name[0] = int(num_and_name[0])
    num_and_name[1] = num_and_name[1].replace(".png", "")
    return num_and_name


def main():
    """Runs the GUI and assigns it a name.
    """
    root = Tk()
    characters_get()
    root.title("Smash Randomiser")
    app = GUI(root)
    root.mainloop()


if __name__ == '__main__':
    """Runs main() if this program hasn't been imported.
    """
    main()
