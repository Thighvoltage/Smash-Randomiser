from tkinter import *
from PIL import Image, ImageTk
import os
from pathlib import Path
import pickle
from random import randrange
from winsound import PlaySound, SND_FILENAME, SND_ASYNC

characters = []
errors = []
DARKNESS_LEVEL = 0.3

class Character:
    def __init__(self, num, name, filename, bright_photo, dark_photo, icon,
                 portrait, head_icon, dark):
        self.num = num
        self.name = name
        self.filename = filename
        self.bright_photo = bright_photo
        self.dark_photo = dark_photo
        self.icon = icon
        self.portrait = portrait
        self.head_icon = head_icon
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
        #self.DARKNESS_LEVEL = 0.3 Moved
        #self.BRIGHTNESS_LEVEL = 1.3 Not in use

        self.master = master
        self.master.configure(bg="gray15")

        self.init_icon_frame()
        self.init_option_frame()
        self.init_portrait_frame()
        self.init_recent_frame()

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
                self.icon_frame, borderwidth=-1, bg=self.BG_COLOUR,
                image=characters[i].bright_photo,
                activebackground=self.BG_COLOUR,
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
            self.all_button, NONE_TEXT, self.deselect_all)
        self.none_button.grid(row=0, column=3, sticky=N)

        self.save_button = clone_widget(
            self.all_button, SAVE_TEXT, self.save_preset)
        self.save_button.grid(row=0, column=0, sticky=N)

        self.load_button = clone_widget(
            self.all_button, LOAD_TEXT, self.load_preset)
        self.load_button.grid(row=0, column=4, sticky=N)

        self.label = Label(
            self.option_frame, bg=self.BG_COLOUR, fg=self.TEXT_COLOUR,
            font=self.FONT)
        self.label.grid(row=1, column=1, columnspan=3)

    def select(self, i):
        """Turns an icon bright."""
        characters[i].icon.configure(image=characters[i].bright_photo)
        characters[i].dark = False

    def deselect(self, i):
        """Turns an icon dark."""
        characters[i].icon.configure(image=characters[i].dark_photo)
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
        """Creates a pool of selected characters and picks a random character
           from it. The chosen character has its name, portrait, and announcer
           clip displayed/played.

           If the pool is empty then an error is displayed and played.
        """
        pool = [characters[i]
                for i in range(len(characters)) if characters[i].dark is False]
        if len(pool) == 0:
            self.display_error()
        else:
            selection = pool[randrange(len(pool))]
            PlaySound(str(Path("Characters/Announcer Clips/"
                      + selection.filename[:-4] + ".wav")),
                      SND_FILENAME | SND_ASYNC)
            self.label.configure(text=selection.name)
            self.display_portrait(selection)
            self.add_to_recent(selection)

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
        """Changes the portrait label to display character's portrait.
           Loads in character's portrait if it does not have one.
        """
        if character.portrait is None:
            portrait_image = Image.open(
                Path("Characters/Portraits/" + character.filename))
            character.portrait = ImageTk.PhotoImage(portrait_image)
        self.portrait_label.configure(image=character.portrait)

    def init_recent_frame(self):
        """Initialises the recent frame."""
        self.recent_frame = Frame(self.master, bg=self.BG_COLOUR)
        self.recent_frame.grid(row=1, column=0, sticky=NE, rowspan=2)

        self.recent_label = Label(
            self.recent_frame, text = "\n\nRecent Characters",
            fg = self.TEXT_COLOUR, bg = self.BG_COLOUR, font=self.FONT)
        self.recent_label.grid(row=0, column=0, columnspan=2)

        self.head_icon_1 = Label(
            self.recent_frame, background=self.BG_COLOUR)
        self.head_icon_1.grid(row=1, column=0)

        self.head_icon_2 = clone_widget(self.head_icon_1)
        self.head_icon_2.grid(row=2, column=0)

        self.head_icon_3 = clone_widget(self.head_icon_1)
        self.head_icon_3.grid(row=3, column=0)

        self.head_icon_label_1 = clone_widget(
        self.recent_label, text="", width=15)
        self.head_icon_label_1.grid(row=1, column=1)

        self.head_icon_label_2 = clone_widget(self.head_icon_label_1)
        self.head_icon_label_2.grid(row=2, column=1)

        self.head_icon_label_3 = clone_widget(self.head_icon_label_1)
        self.head_icon_label_3.grid(row=3, column=1)

    def add_to_recent(self, character):
        """Adds a character to the top of the recent characters list and moves
           the rest down.
        """
        self.head_icon_3.configure(image=self.head_icon_2.cget('image'))
        self.head_icon_2.configure(image=self.head_icon_1.cget('image'))

        self.head_icon_label_3.configure(text=self.head_icon_label_2.cget('text'))
        self.head_icon_label_2.configure(text=self.head_icon_label_1.cget('text'))

        if character.head_icon is None:
            head_icon_image = Image.open(
                Path("Characters/Head Icons/" + character.filename))
            head_icon_image = head_icon_image.resize((70, 70), Image.ANTIALIAS)
            character.head_icon = ImageTk.PhotoImage(head_icon_image)

        self.head_icon_1.configure(image=character.head_icon)
        self.head_icon_label_1.configure(text=character.name)


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
        bright_photo = ImageTk.PhotoImage(image)
        dark_photo = ImageTk.PhotoImage(image.point(
            lambda p: p * DARKNESS_LEVEL))

        filename = name
        num_and_name = character_num_and_name(icon_names[i])
        characters.append(Character(num_and_name[0], num_and_name[1], filename,
                                    bright_photo, dark_photo, None, None, None,
                                    False))
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
