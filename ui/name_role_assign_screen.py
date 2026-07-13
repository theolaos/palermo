# palermo, an automatic narrator to play with all of your buddies
# Copyright (C) 2026  theolaos

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from logic import *


class PerScreen(BoxLayout):
    def __init__(self, carousel, **kwargs):
        super().__init__(**kwargs)
        self.carousel = carousel


class NameRoleAssignScreen(Screen):
    def on_enter(self):
        screen_carousel = self.ids.my_carousel
        screen_carousel.clear_widgets()

        # name_dict = {}
        # for role in roles:
        for i in range(Data.players):
            screen_carousel.add_widget(
                PerScreen(carousel=screen_carousel)
            )