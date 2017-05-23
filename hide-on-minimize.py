# COPYRIGHT (c) 2016 mice7r <mice7r@gmail.com>
#
# GNU GENERAL PUBLIC LICENSE
#    Version 3, 29 June 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from gi.repository import GObject, Peas, Gtk

class HideOnMinimize(GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(HideOnMinimize, self).__init__()

    def do_activate(self):
        self.window = self.object.get_property("window")
        self.shell = self.object
        self.player = self.shell.props.shell_player

        self.window_handler_id = self.window.connect("window-state-event", self.state_event)
        self.player_handler_id = self.player.connect("playing-changed", self.playing_changed)

    def do_deactivate(self):
        self.window.show()
        self.window.disconnect(self.window_handler_id)
        self.player.disconnect(self.player_handler_id)

    def playing_changed(self, player, playing):
        if not playing:
            self.window.show()
            self.window.deiconify()

    def state_event(self, widget, event):
        widget_state = widget.get_window().get_state()

        # minimized and playing
        if widget_state == 2 and self.player.props.playing:
            self.window.hide()

        return True
