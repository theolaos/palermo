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
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.metrics import dp


from logic import *

class InputAmountPlayers(BoxLayout):
    def validate_player_count(self, text):
        # Grab the TextInput widget using its ID
        input_field = self.ids.player_count_input
        
        try:
            value = int(text)
            Data.players = value
            if value < 4:
                input_field.text = "4"
                Data.players = 4
        except ValueError:
            # If the field was left entirely blank, default it to 4
            input_field.text = "4"
            Data.players = 4

        
    def get_text(self) -> str:
        return str(Data.players)


class RoleItem(BoxLayout):
    # Properties that can be passed from KV or updated dynamically
    count = NumericProperty(0)
    emoji = StringProperty("")
    role_name = StringProperty("")
    short_desc = StringProperty("")
    long_desc = StringProperty("")
    is_expanded = BooleanProperty(False) 
    
    def __init__(self, role_class, **kwargs):
        super().__init__(**kwargs)
        self.role_class = role_class

    def toggle_expand(self, touch):
        # Check if the touch actually happened inside this specific widget
        if self.collide_point(*touch.pos):
            # If the user clicked the step buttons, don't expand/collapse
            if self.ids.minus_btn.collide_point(*touch.pos) or self.ids.plus_btn.collide_point(*touch.pos):
                return
            
            # Toggle the expansion state
            if not self.is_expanded:
                self.height = dp(180)  # Expanded height
                self.ids.extra_desc.text = self.long_desc
                self.is_expanded = True
            else:
                self.height = dp(80)   # Collapsed height
                self.ids.extra_desc.text = ""
                self.is_expanded = False


    def increment(self):
        temp = Data.amount_roles.copy()
        temp[self.role_class] += 1

        try:
            verify_role_dict(Data.players, temp)
            Data.amount_roles[self.role_class] += 1
            self.count = Data.amount_roles[self.role_class]
        except TooManyRoles as e:
            print("Whoops TooManyRoles")
        except UnBalanced as e:
            print("Whoops UnBalanced")


    def decrement(self):
        if self.count > 0:
            Data.amount_roles[self.role_class] -= 1
            self.count = Data.amount_roles[self.role_class]

    def sync(self):
        self.count = Data.amount_roles[self.role_class]


class RoleSelectionScreen(Screen):
    def on_enter(self):
        """ This method triggers automatically when the screen displays. """
        # clear any old items so they dont duplicate if you leave and come back
        container = self.ids.roles_container
        container.clear_widgets()

        container.add_widget(InputAmountPlayers())
        
        # create and append the widgets dynamically using python
        self.role_item_list = []
        for role in roles_list:
            item = RoleItem(
                role_class=role,
                count=Data.amount_roles[role],
                emoji=role.data["emoji"],
                role_name=role.data["role"],
                short_desc=role.data["short"],
                long_desc=role.data["long"]
            )
            self.role_item_list.append(item)
            container.add_widget(item)


    def default_roles(self):
        default_role_dict(Data.players, Data.amount_roles)
        for role_item in self.role_item_list:
            role_item.sync()