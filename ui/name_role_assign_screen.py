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

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, BooleanProperty

from logic import *


class PressableLabel(BoxLayout):
    display_text = StringProperty("Πάτα για να μάθεις τον ρόλο σου. 🔎")
    bg_color = ListProperty([0.15, 0.15, 0.15, 1]) # Default Dark Gray


    def __init__(self, role, **kwargs):
        super().__init__(**kwargs)
        self.role = role
        self.data = role.data


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Change text and color to indicate pressing
            self.display_text = f"{self.data["emoji"]} Είσαι {self.data["role"]} {self.data["emoji"]}"
            self.bg_color = [0.2, 0.6, 1, 1] # Change to Blue
            return True # Consumes the touch event
        return super().on_touch_down(touch)
    

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.display_text = "Πάτα για να μάθεις τον ρόλο σου. 🔎"
            self.bg_color = [0.15, 0.15, 0.15, 1] # Back to Dark Gray
            return True
        return super().on_touch_up(touch)


class PerScreen(BoxLayout):
    prev_screen = BooleanProperty(False)
    next_screen = BooleanProperty(False) 
    bg_color1 = ListProperty([0.15, 0.15, 0.15, 1]) # Default Dark Gray

    def __init__(self, carousel, **kwargs):
        super().__init__(**kwargs)
        self.carousel = carousel
        
        self.ids.reavel_role_label.add_widget(
            PressableLabel(Citizen)
        )


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