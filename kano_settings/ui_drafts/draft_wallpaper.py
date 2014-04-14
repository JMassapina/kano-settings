#!/usr/bin/env python

# set_wallpaper.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

from gi.repository import Gtk, GdkPixbuf
import kano_settings.config_file as config_file
#import kano_settings.components.heading as heading
import kano_settings.components.fixed_size_box as fixed_size_box
import kano_settings.constants as constants

selected_button = 0
initial_button = 0
NUMBER_OF_COLUMNS = 4
# Calculate this dynamically once we have data about pictures
NUMBER_OF_ROWS = 2
COLUMN_PADDING = 10
ROW_PADDING = 10


def activate(_win, box, update):
    global selected_button, initial_button

    wallpaper_array = ["Icon-Audio", "Icon-Display", "Icon-Overclocking", "Icon-Keyboard", "Icon-Email", "Icon-Mouse"]

    title = Gtk.Label("Choose your background")
    title.get_style_context().add_class('title')
    images = []
    boxes = []

    wallpaper_table = Gtk.Table(NUMBER_OF_ROWS, NUMBER_OF_COLUMNS, True)
    wallpaper_table.set_row_spacings(20)
    wallpaper_table.set_col_spacings(20)

    for i in range(len(wallpaper_array)):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(constants.media + "/Icons/" + wallpaper_array[i] + ".png", 100, 100)
        image = Gtk.Image()
        image.get_style_context().add_class('wallpaper_box')
        image.set_from_pixbuf(pixbuf)
        images.append(image)
        backgroundbox = Gtk.Button()
        backgroundbox.add(image)
        backgroundbox.connect('button_press_event', set_wallpaper, wallpaper_array[i])
        #backgroundbox.get_style_context().add_class('background_box')
        boxes.append(backgroundbox)

    settings = fixed_size_box.Fixed()

    # Attach to table
    index = 0
    row = 0

    while index < len(wallpaper_array):
        for j in range(NUMBER_OF_COLUMNS):
            if index < len(wallpaper_array):
                wallpaper_table.attach(boxes[index], j, j + 1, row, row + 1,
                                       Gtk.AttachOptions.EXPAND, Gtk.AttachOptions.EXPAND, 0, 0)
                index += 1
            else:
                grey_box = Gtk.Button()
                grey_box.set_size_request(100, 100)
                grey_box.get_style_context().add_class('grey_box')
                grey_box.connect('button_press_event', set_wallpaper, "grey_box")
                wallpaper_table.attach(grey_box, j, j + 1, row, row + 1,
                                       Gtk.AttachOptions.EXPAND, Gtk.AttachOptions.EXPAND, 0, 0)
                index += 1
        row += 1

    settings.box.pack_start(wallpaper_table, False, False, 10)

    # Add apply changes button under the main settings content
    box.pack_start(title, False, False, 0)
    box.pack_start(settings.box, False, False, 0)
    box.pack_start(update.box, False, False, 0)
    update.enable()


def set_wallpaper(widget=None, event=None, name=""):
    print "name = " + str(name)


def apply_changes(button):

    #  Mode   speed
    # Slow     1
    # Normal  default
    # High     10

    # Mode has no changed
    if initial_button == selected_button:
        return

    config = "Slow"
    # Slow configuration
    if selected_button == 0:
        config = "Slow"
    # Modest configuration
    elif selected_button == 1:
        config = "Normal"
    # Medium configuration
    elif selected_button == 2:
        config = "Fast"

    # Update config
    config_file.replace_setting("Mouse", config)