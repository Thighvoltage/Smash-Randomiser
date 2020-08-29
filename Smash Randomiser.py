from tkinter import *
from PIL import Image, ImageTk
import os
from pathlib import Path
import pickle
from random import randrange
from winsound import PlaySound, SND_FILENAME, SND_ASYNC

characters = []
errors = []

class Character:
    def __init__(self, num, name, filename, image, photo, icon, portrait,
                 display, dark):
        self.num = num
        self.name = name
        self.filename = filename
        self.image = image
        self.photo = photo
        self.icon = icon
        self.portrait = portrait
        self.display = display
        self.dark = dark


class Error:
    def __init__(self, name, photo):
        self.name = name
        self.photo = photo


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

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)

    def init_icon_frame(self):
        """Initialises and fills the icon frame."""
        self.icon_frame = Frame(self.master, bg=self.BG_COLOUR)
        self.icon_frame.grid(row=0, column=0, sticky=N)
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
        self.option_frame.grid(row=1, column=0, sticky=N)

        self.select_button = Button(
            self.option_frame, text=SELECT_TEXT, command=self.select_character,
            width=20, height=1, font=self.FONT, fg=self.TEXT_COLOUR,
            bg=self.BG_COLOUR2, activebackground=self.BG_COLOUR2,
            activeforeground=self.TEXT_COLOUR)
        self.select_button.grid(row=0, column=2, sticky=N)

        self.all_button = clone_widget(
            self.select_button, ALL_TEXT, self.select_all, width=10, height=1)
        self.all_button.grid(row=0, column=1, sticky=N)

        self.none_button = clone_widget(
            self.select_button, NONE_TEXT, self.deselect_all, width=10,
            height=1)
        self.none_button.grid(row=0, column=3, sticky=N)

        self.save_button = clone_widget(
            self.select_button, SAVE_TEXT, self.save_preset, width=10,
            height=1)
        self.save_button.grid(row=0, column=0, sticky=N)

        self.load_button = clone_widget(
            self.select_button, LOAD_TEXT, self.load_preset, width=10,
            height=1)
        self.load_button.grid(row=0, column=4, sticky=N)

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

    def select_character(self):
        """TBW
        """
        pool = [characters[i]
                for i in range(len(characters)) if characters[i].dark is False]
        try:
            selection = randrange(len(pool))
        except ValueError:
            self.display_error()
        else:
            PlaySound(str(Path("Characters/Announcer Clips/"
                      + pool[selection].filename[:-4] + ".wav")),
                      SND_FILENAME | SND_ASYNC)
            self.label.configure(text=pool[selection].name)
            self.display_portrait(pool[selection])

    def display_error(self):
        """Sets portrait_label to Navi, plays Navi sound effect, and changes
           the response label.
        """
        selection = randrange(len(errors))
        PlaySound(str(Path("Errors/Sounds/" + errors[selection].name + ".wav")), SND_FILENAME | SND_ASYNC)

        self.portrait_label.configure(image=errors[selection].photo)
        self.label.configure(text="Select a character silly!")

    def init_portrait_frame(self):
        """Initialises the portrait frame."""
        self.portrait_frame = Frame(self.master, bg=self.BG_COLOUR)
        self.portrait_frame.grid(row=2, column=0, sticky=N)

        self.portrait_label = Label(
            self.portrait_frame, background=self.BG_COLOUR)
        self.portrait_label.grid(row=0, column=0)

    def display_portrait(self, character):
        """asd"""
        if character.portrait is None:
            portrait_image = Image.open(
                Path("Characters/Portraits/" + character.filename))
            character.portrait = ImageTk.PhotoImage(portrait_image)
        self.portrait_label.configure(image=character.portrait)


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


def get_characters():
    """Gets the image and name data for each character then creates a
       class for each.
    """
    icon_names = [name for name in os.listdir("Characters/Icons")]
    portrait_names = [name for name in os.listdir("Characters/Portraits")]

    for i, name in enumerate(icon_names):
        image = Image.open(Path("Characters/Icons/" + name))
        photo = ImageTk.PhotoImage(image)

        filename = name
        num_and_name = character_num_and_name(icon_names[i])
        characters.append(Character(num_and_name[0], num_and_name[1], filename,
                                    image, photo, None, None, None, False))
    characters.sort(key=lambda x: x.num)


def character_num_and_name(icon_name):
    """Returns [num, name] for a string of the format 'num-name.png' where
       .png can be any four character file extension (including '.').
    """
    num_and_name = icon_name.split("-")
    num_and_name[0] = int(num_and_name[0])
    num_and_name[1] = num_and_name[1][:-4]
    return num_and_name


def get_errors():
    """asd"""
    for name in os.listdir(Path("Errors/Images")):
        image = Image.open(Path("Errors/Images/" + name))
        photo = ImageTk.PhotoImage(image)
        errors.append(Error(name[:-4], photo))


def main():
    """Runs the GUI and assigns it a name.
    """
    root = Tk()
    get_characters()
    get_errors()
    root.title("Smash Randomiser")
    root.iconbitmap(Path("Images/" + "Smash ball.ico"))
    app = GUI(root)
    root.mainloop()


if __name__ == '__main__':
    """Runs main() if this program hasn't been imported.
    """
    main()
