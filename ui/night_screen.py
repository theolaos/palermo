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
from kivy.properties import StringProperty, ListProperty, BooleanProperty

from logic import *


class PlayerItem(BoxLayout):
    action_button_text = StringProperty("Action")
    player_name = StringProperty("Name")
    emoji = StringProperty("👤")
    show_role_emoji = BooleanProperty(False)
    default_emoji = StringProperty("👤")


    def __init__(self, player, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        # self.default_emoji = "👤"
    

    def vote(self):
        self.player.vote += 1


class NightScreen(Screen):
    bottom_button = StringProperty("PAUSE")
    bottom_bg_color = ListProperty((0.2, 0.8, 0.4, 1))
    current_text = StringProperty("Μια νέα Νύχτα στο Παλέρμο")

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.introductory_night = False # turns to True if it happened.
        self.overlay = None

    def on_enter(self):
        print("yooooo biatch")
        Data.day += 1
        container = self.ids.players_container_night
        container.clear_widgets()
        
        # create and append the widgets dynamically
        self.role_item_list = []
        for player in Data.assigned_players:
            item = PlayerItem(
                player=player,
                player_name=player.name,
                emoji=player.role.data["emoji"]
            )
            self.role_item_list.append(item)
            container.add_widget(item)

        if Data.current_state == GamePhase.FIRST_NIGHT:
            ...
            
        else:
            ...
            


    def show_overlay(self):
        if not self.overlay: # dynamic overlay creation
            from kivy.factory import Factory
            self.overlay = Factory.LoadingOverlay()
        
        # Open the overlay to lock controls and show the text
        self.overlay.open()


    def press_next_day(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'day_voting_screen'       
