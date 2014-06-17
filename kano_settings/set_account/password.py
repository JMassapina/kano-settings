#!/usr/bin/env python
#
# password.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Controls the UI of the change password screen

from gi.repository import Gtk, Gdk, GObject
import threading
from kano.gtk3.heading import Heading
import kano_settings.components.fixed_size_box as fixed_size_box
import kano.utils as utils
import pam
import kano.gtk3.kano_dialog as kano_dialog

win = None
entry1 = None
entry2 = None
entry3 = None
button = None


def activate(_win, changeable_content, _button):
    global win, entry1, entry2, entry3, button

    win = _win
    settings = fixed_size_box.Fixed()
    button = _button

    entry1 = Gtk.Entry()
    entry1.set_size_request(300, 44)
    entry1.props.placeholder_text = "Old password"
    entry1.set_visibility(False)
    entry2 = Gtk.Entry()
    entry2.props.placeholder_text = "New password"
    entry2.set_visibility(False)
    entry3 = Gtk.Entry()
    entry3.props.placeholder_text = "Repeat new password"
    entry3.set_visibility(False)

    entry1.connect("key_release_event", enable_button, _button)
    entry2.connect("key_release_event", enable_button, _button)
    entry3.connect("key_release_event", enable_button, _button)

    # Entry container
    entry_container = Gtk.Grid(column_homogeneous=False,
                               column_spacing=22,
                               row_spacing=10)

    entry_container.attach(entry1, 0, 0, 1, 1)
    entry_container.attach(entry2, 0, 1, 1, 1)
    entry_container.attach(entry3, 0, 2, 1, 1)

    align = Gtk.Alignment(xalign=0.5, yalign=0, xscale=0, yscale=0)
    align.add(entry_container)
    settings.box.pack_start(align, False, False, 0)
    _button.set_sensitive(False)
    title = Heading("Change your password", "Keep out the baddies!")

    changeable_content.pack_start(title.container, False, False, 0)
    changeable_content.pack_start(settings.box, False, False, 0)
    changeable_content.pack_start(_button.align, False, False, 10)

    win.show_all()


def apply_changes(button):
    global win

    # This is a callback called by the main loop, so it's safe to
    # manipulate GTK objects:
    watch_cursor = Gdk.Cursor(Gdk.CursorType.WATCH)
    win.get_window().set_cursor(watch_cursor)
    button.set_sensitive(False)

    def lengthy_process():
        global button

        old_password = entry1.get_text()
        new_password1 = entry2.get_text()
        new_password2 = entry3.get_text()

        # Verify the current password in the first text box
        # Get current username
        username, e, num = utils.run_cmd("echo $SUDO_USER")
        # Remove trailing newline character
        username = username.rstrip()

        if not pam.authenticate(username, old_password):
            title = "Could not change password"
            description = "Your old password is incorrect!"
        # If the two new passwords match
        elif new_password1 == new_password2:
            out, e, cmdvalue = utils.run_cmd("echo $SUDO_USER:%s | sudo chpasswd" % (new_password1))
            # if password is not changed
            if cmdvalue != 0:
                title = "Could not change password"
                description = "Your new password is not long enough or contains special characters."
            else:
                title = "Password changed!"
                description = ""
        else:
            title = "Could not change password"
            description = "Your new passwords don't match!  Try again"

        def done(title, description):
            create_dialog(title, description)
        GObject.idle_add(done, title, description)

    thread = threading.Thread(target=lengthy_process)
    thread.start()
    return -1


def create_dialog(message1="Could not change password", message2=""):
    global win, button

    kdialog = kano_dialog.KanoDialog(message1, message2,
                                     {"TRY AGAIN": {"return_value": -1}})
    response = kdialog.run()
    win.get_window().set_cursor(None)
    button.set_sensitive(True)
    return response


def clear_text():
    global entry1, entry2, entry3
    entry1.set_text("")
    entry2.set_text("")
    entry3.set_text("")


def enable_button(widget=None, event=None, apply_changes=None):
    text1 = entry1.get_text()
    text2 = entry2.get_text()
    text3 = entry3.get_text()
    apply_changes.set_sensitive(text1 != "" and text2 != "" and text3 != "")
