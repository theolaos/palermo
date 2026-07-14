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

from functools import partial
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.clock import Clock


from logic import *
from script import SoundManager


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

        self.stages = None

        self.night_stages = [
            "night_intro",
            "night_start_mafia",
            "night_mafia_target",
            Choice(Killer),
            "night_people_close",
            "night_cop_open",
            Choice(Sheriff),
            "night_person_close",
        ]

        self.intro_stages = [
            "night_intro",
            "night_start_mafia",
            Wait(6),
            "night_people_close",
            "intro_spy_mafia",
            Wait(6.0),
            "night_person_close",
            "night_cop_open",
            Choice(Sheriff),
            "night_person_close",
            "intro_madness"
        ]

        # for k, v in Data.amount_roles.items():
        #     if v > 0:
        #         self.intro_stages = 

        self.index = 0
        self.clock_event = None


    def on_enter(self):
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

        self.stages = self.intro_stages if Data.current_state == GamePhase.FIRST_NIGHT else self.night_stages

        self.show_overlay()
        self.play_stage()


    def show_overlay(self):
        if not self.overlay: # dynamic overlay creation
            from kivy.factory import Factory
            self.overlay = Factory.LoadingOverlay()
        
        # Open the overlay to lock controls and show the text
        self.overlay.open()

    
    def start_choice(self):
        ...


    def timer_overlay(self):
        ...

    
    def choice(self):
        ...


    def play_stage(self):
        if self.index > len(self.stages):
            self.overlay.dismiss()
            self.manager.transition.direction = 'left'
            self.manager.current = 'day_voting_screen'
            return

        stage = self.stages[self.index]

        if type(stage) == Wait:
            callback = partial(self.timer_overlay, stage.sec)
            self.clock_event = Clock.schedule_once(callback, stage.sec)    
            return
        elif type(stage) == Choice:
            self.overlay.dismiss()
            self.choice(stage.whos)
            return
        
        SoundManager.play_narration(stage)
        self.clock_event = Clock.schedule_once(self.next_stage, SoundManager.get_length(stage))
        

    def next_stage(self, dt=None):
        self.index += 1
        self.play_stage()


    def pause_narration(self):
        SoundManager.stop_narration()


    def resume_narration(self):
        SoundManager.continue_narration()
