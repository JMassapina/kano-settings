#!/usr/bin/env python

# set_mouse.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

from gi.repository import Gdk
from kano_settings.templates import RadioButtonTemplate
from .config_file import get_setting, set_setting
from kano_settings.data import get_data
from kano_settings.system.mouse import change_mouse_speed


class SetMouse(RadioButtonTemplate):
    selected_button = 0
    initial_button = 0

    data = get_data("SET_MOUSE")

    def __init__(self, win):
        title = self.data["LABEL_1"]
        description = self.data["LABEL_2"]
        kano_label = self.data["KANO_BUTTON"]
        option1 = self.data["OPTION_1"]
        desc1 = self.data["DESCRIPTION_1"]
        option2 = self.data["OPTION_2"]
        desc2 = self.data["DESCRIPTION_2"]
        option3 = self.data["OPTION_3"]
        desc3 = self.data["DESCRIPTION_3"]

        RadioButtonTemplate.__init__(self, title, description, kano_label,
                                     [[option1, desc1],
                                      [option2, desc2],
                                      [option3, desc3]])
        self.win = win
        self.win.set_main_widget(self)

        # Show the current setting by electing the appropriate radio button
        self.current_setting()
        self.selected_button = self.initial_button
        self.get_button(self.initial_button).set_active(True)

        self.win.top_bar.enable_prev()
        self.win.change_prev_callback(self.reset_and_go_home)

        self.kano_button.connect("button-release-event", self.set_mouse)
        self.kano_button.connect("key-release-event", self.set_mouse)

        self.win.show_all()

    def reset_and_go_home(self, widget=None, event=None):
        self.selected_button = self.initial_button
        self.get_button(self.initial_button).set_active(True)
        self.win.go_to_home()

    def set_mouse(self, button, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:

            #  Mode   speed
            # Slow     1
            # Normal  default
            # High     10

            # Mode has no changed
            if self.initial_button == self.selected_button:
                self.win.go_to_home()
                return

            config = "Slow"
            # Slow configuration
            if self.selected_button == 0:
                config = "Slow"
            # Modest configuration
            elif self.selected_button == 1:
                config = "Normal"
            # Medium configuration
            elif self.selected_button == 2:
                config = "Fast"

            # Update config
            set_setting("Mouse", config)
            self.win.go_to_home()

    def current_setting(self):
        mouse = get_setting("Mouse")
        if mouse == "Slow":
            self.initial_button = 0
        elif mouse == "Normal":
            self.initial_button = 1
        elif mouse == "Fast":
            self.initial_button = 2

    def on_button_toggled(self, button):

        if button.get_active():
            label = button.get_label()
            if label == "Slow":
                self.selected_button = 0
            elif label == "Normal":
                self.selected_button = 1
            elif label == "Fast":
                self.selected_button = 2

            # Apply changes so speed can be tested
            change_mouse_speed(self.selected_button)

