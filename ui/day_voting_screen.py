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
from kivy.properties import StringProperty, ListProperty


class NightScreen(Screen):
    bottom_button = StringProperty("PAUSE")
    bottom_bg_color = ListProperty((0.2, 0.8, 0.4, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.introductory_night = False # turns to True if it happened.
    

    def on_enter(self):
        container = self.ids.players_container
        container.clear_widgets()
        
        # create and append the widgets dynamically using python
        self.role_item_list = []
        for role in roles_list:
            item = PlayerItem(

            )
            self.role_item_list.append(item)
            container.add_widget(item)

        if Data.current_state == GamePhase.FIRST_NIGHT:
            ...
            
        else:
            ...
            

    def press_next_day(self):
        self.transition.direction = 'left'
        self.current = 'day_voting_screen'        
        

class PlayerItem(BoxLayout):
    ...