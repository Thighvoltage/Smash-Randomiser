from tkinter import *
from PIL import Image, ImageTk
import os
# import os.path
import pickle
from random import randint
from winsound import PlaySound, SND_FILENAME, SND_ASYNC

characters = []


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
        self.FONT = ("Helvetica", "12")
        self.DARKNESS_LEVEL = 0.3
        self.BRIGHTNESS_LEVEL = 1.3

        self.master = master
        self.master.configure(bg="gray15")

        self.init_icon_frame()
        self.init_option_frame()
        self.init_portrait_frame()

    def init_icon_frame(self):
        """Initialises and fills the icon frame."""
        self.icon_frame = Frame(self.master, background=self.BG_COLOUR)
        self.icon_frame.grid(row=0, column=0, columnspan=2, sticky="nesw")
        self.display_icons()

    def display_icons(self):
        """Creates a button for each character and arranges them in
           order in the icon frame.
        """
        LENGTH = 12
        HEIGHT = len(characters) // LENGTH + 1
        FREE_SPACE = LENGTH - len(characters) % LENGTH
        LEFT_SPACE = FREE_SPACE // 2

        for i in range(len(characters)):
            characters[i].icon = Button(
                self.icon_frame, image=characters[i].photo, borderwidth=-1,
                bg=self.BG_COLOUR, activebackground=self.BG_COLOUR,
                command=lambda i=i: self.select_icon(i))

            if i//LENGTH != HEIGHT-1:
                characters[i].icon.grid(row=i//LENGTH, column=i % LENGTH)
            else:
                characters[i].icon.grid(
                    row=HEIGHT, column=i % LENGTH + LEFT_SPACE)
                if FREE_SPACE % 2 != 0:
                    characters[i].icon.grid(columnspan=2)

    def init_option_frame(self):
        """Initialises and fills the option frame."""
        SELECT_TEXT = "Select a Character"
        ALL_TEXT = "Select All"
        NONE_TEXT = "Select None"
        SAVE_TEXT = "Save Preset"
        LOAD_TEXT = "Load Preset"

        self.option_frame = Frame(self.master, bg=self.BG_COLOUR)
        self.option_frame.grid(row=1, column=1, sticky=NW)

        self.select_button = Button(
            self.option_frame, text=SELECT_TEXT, command=self.select_character,
            width=20, height=1, font=self.FONT, fg=self.TEXT_COLOUR,
            bg=self.BG_COLOUR2, activebackground=self.BG_COLOUR2,
            activeforeground=self.TEXT_COLOUR)
        self.select_button.grid(row=0, column=2, sticky=NW)

        self.all_button = clone_widget(
            self.select_button, ALL_TEXT, self.select_all, width=10, height=1)
        self.all_button.grid(row=0, column=1, sticky=NW)

        self.none_button = clone_widget(
            self.select_button, NONE_TEXT, self.deselect_all, width=10,
            height=1)
        self.none_button.grid(row=0, column=3, sticky=NW)

        self.save_button = clone_widget(
            self.select_button, SAVE_TEXT, self.save_preset, width=10,
            height=1)
        self.save_button.grid(row=0, column=0, sticky=NW)

        self.load_button = clone_widget(
            self.select_button, LOAD_TEXT, self.load_preset, width=10,
            height=1)
        self.load_button.grid(row=0, column=4, sticky=NW)

        self.label = Label(
            self.option_frame, bg=self.BG_COLOUR, fg=self.TEXT_COLOUR,
            font=self.FONT)
        self.label.grid(row=1, column=1, columnspan=3)

    def select(self, i):
        """Turns an icon bright."""
        characters[i].photo = ImageTk.PhotoImage(characters[i].image)
        characters[i].icon.configure(image=characters[i].photo)
        characters[i].dark = False

    def deselect(self, i):
        """Turns an icon dark."""
        characters[i].photo = ImageTk.PhotoImage(characters[i].image.point(
            lambda p: p * self.DARKNESS_LEVEL))
        characters[i].icon.configure(image=characters[i].photo)
        characters[i].dark = True

    def select_all(self):
        """Turns all icons bright."""
        for i in range(len(characters)):
            if characters[i].dark is True:
                self.select(i)

    def deselect_all(self):
        """Turns all icons dark."""
        for i in range(len(characters)):
            if characters[i].dark is False:
                self.deselect(i)

    def select_icon(self, i):
        """Turns an icon dark if it's bright, or turns an icon bright
           if it's dark.
        """
        if characters[i].dark is True:
            self.select(i)
        else:
            self.deselect(i)

    def save_preset(self):
        """Writes the dark value of each character to a file."""
        pickle_out = open("Smash Randomiser Preset", "wb")
        pickle.dump([characters[i].dark for i in range(len(characters))],
                    pickle_out)
        pickle_out.close()

        self.label.configure(text="Saved!")

    def load_preset(self):
        """Loads the preset file, updates the dark values of each
           character, and updates the GUI.
        """
        try:
            pickle_in = open("Smash Randomiser Preset", "rb")
        except FileNotFoundError:
            self.label.configure(text="No preset!")
        else:
            dark_values = pickle.load(pickle_in)
            pickle_in.close()

            for i in range(len(characters)):
                if characters[i].dark != dark_values[i]:
                    characters[i].dark = dark_values[i]
                    if characters[i].dark is False:
                        self.select(i)
                    else:
                        self.deselect(i)

            self.label.configure(text="Loaded!")

    def init_portrait_frame(self):
        """Initialises the portrait frame."""
        self.portrait_frame = Frame(self.master, bg=self.BG_COLOUR)
        self.portrait_frame.grid(row=1, column=0, sticky=NW)

    def select_character(self):
        """TBW
        """
        pool = [characters[i]
                for i in range(len(characters)) if characters[i].dark is False]
        try:
            selection = randint(1, len(pool)) - 1
        except ValueError:
            self.label.configure(text="Select a character silly!")
            if randint(0, 1) == 0:
                PlaySound(os.getcwd() + "\\Sound Effects\\Hey.wav",
                          SND_FILENAME | SND_ASYNC)
            else:
                PlaySound(os.getcwd() + "\\Sound Effects\\Listen.wav",
                          SND_FILENAME | SND_ASYNC)
        else:
            self.label.configure(text=pool[selection].name)
            PlaySound(
                os.getcwd() + "\\Announcer Clips\\" + str(pool[selection].num)
                + "-" + pool[selection].name + ".wav",
                SND_FILENAME | SND_ASYNC)


def get_characters():
    """Gets the image and name data for each character then creates a
       class for each.
    """
    icon_names = [name for name in
                  os.listdir(os.getcwd() + "\\Character Icons")]
    portrait_names = [name for name in
                      os.listdir(os.getcwd() + "\\Character Portraits")]

    for i, name in enumerate(icon_names):
        image = Image.open(os.getcwd() + "\\Character Icons\\" + name)
        photo = ImageTk.PhotoImage(image)
        # portrait_image = Image.open(
        #    os.getcwd()+"\\Character Portraits\\"+str(name))
        # portrait_photo = ImageTk.PhotoImage(portrait_image)

        num_and_name = character_num_and_name(icon_names[i])
        characters.append(Character(num_and_name[0], num_and_name[1],
                                    image, photo, None, None, None, False))
    characters.sort(key=lambda x: x.num)


def character_num_and_name(icon_name):
    """Returns [num, name] for """
    num_and_name = icon_name.split("-")
    num_and_name[0] = int(num_and_name[0])
    num_and_name[1] = num_and_name[1].replace(".png", "")
    return num_and_name


def clone_widget(widget, text=None, command=None, width=None, height=None):
    """Returns a clone of widget.
       Some elements can be modified with optional parameters.
    """
    parent = widget.nametowidget(widget.winfo_parent())
    cls = widget.__class__

    clone = cls(parent)
    for key in widget.configure():
        clone.configure({key: widget.cget(key)})

    clone.configure(text=text, command=command, width=width, height=height)
    return clone


def main():
    """Runs the GUI and assigns it a name.
    """
    root = Tk()
    get_characters()
    root.title("Smash Randomiser")
    root.iconbitmap(os.getcwd() + "\\Images\\" + "Smash ball.ico")
    app = GUI(root)
    root.mainloop()


if __name__ == '__main__':
    """Runs main() if this program hasn't been imported.
    """
    main()
