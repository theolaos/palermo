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
from kivy.app import App


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
    has_prev = BooleanProperty(False)
    has_next = BooleanProperty(False) 
    bg_color1 = ListProperty([0.15, 0.15, 0.15, 1]) # Default Dark Gray
    bottom_button_text = StringProperty("NEXT")
    name = StringProperty("")

    def __init__(self, carousel, role, **kwargs):
        super().__init__(**kwargs)
        self.carousel = carousel
        self.role = role
        
        self.pressable_label = PressableLabel(role)

        self.ids.reavel_role_label.add_widget(
            self.pressable_label
        )


    def bottom_button(self):
        if self.has_next:
            self.carousel.load_next()
        else:
            root = App.get_running_app().root 
            root.transition.direction = 'up'
            root.current = 'name_role_assign_screen'

    
    def top_button(self):
        if self.has_prev:
            self.carousel.load_previous()
        else:
            root = App.get_running_app().root 
            root.transition.direction = 'down'
            root.current = 'role_selection_screen'

    
    def save_user_data(self, text_value) -> None:
        if self.name != text_value:
            temp = Data.assigned_roles.pop(self.name, None)
            Data.assigned_roles[text_value] = self.role
            self.name = text_value
        
        print(Data.assigned_roles)


class NameRoleAssignScreen(Screen):
    def on_enter(self):
        screen_carousel = self.ids.my_carousel
        screen_carousel.clear_widgets()

        Data.pre_assign_roles = generate_pre_assign_roles_list(Data.amount_roles)

        # name_dict = {}
        # for role in roles:
        for i in range(Data.players):
            has_prev = i > 0
            has_next = i < Data.players

            bottom_button = "NEXT"
            if i + 1 == Data.players:
                bottom_button = "START GAME"

            screen_carousel.add_widget(PerScreen(
                carousel=screen_carousel,
                role=Data.pre_assign_roles[i],
                has_prev=has_prev,
                has_next=has_next,
                bottom_button_text=bottom_button
            ))