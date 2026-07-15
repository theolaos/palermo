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
from kivy.uix.modalview import ModalView

from kivy.properties import StringProperty, ListProperty, BooleanProperty, ObjectProperty, ColorProperty
from kivy.clock import Clock

from logic import *
from script import SoundManager


class PlayerItem(BoxLayout):
    action_button_text = StringProperty("Action")
    player_name = StringProperty("Name")
    emoji = StringProperty("👤")
    show_role_emoji = BooleanProperty(False)
    default_emoji = StringProperty("👤")
    bg_color = ColorProperty([1,1,1,1])


    def __init__(self, player, screen, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        self.screen = screen
        # self.default_emoji = "👤"
    

    def vote(self):
        if Data.current_state in [GamePhase.FIRST_NIGHT, GamePhase.NIGHT] and Data.night_action:
            if self.player.role == Sheriff:
                return

            self.action_button_text = "Revealed" if Data.night_action_role == Sheriff else "Killed"
            self.show_role_emoji = Data.night_action_role == Sheriff 

            Data.night_action = False

            self.screen.revealed(self.player)
        else:
            self.player.vote += 1

# import os
# print("Font path exists:", os.path.exists("ui/fonts/twemoji.ttf"))

class NightScreen(Screen):
    bottom_button = StringProperty("PAUSE")
    bottom_bg_color = ListProperty((0.2, 0.8, 0.4, 1))
    current_text = StringProperty("Μια νέα Νύχτα στο Παλέρμο")

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.introductory_night = False # turns to True if it happened.
        self.overlay = None
        self.overlay_open = False

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
            OverlayText("Νεα νύχτα"),
            "night_intro",
            OverlayText("Δολοφόνοι"),
            "night_start_mafia",
            Wait(6.0),
            "night_people_close",
            OverlayText("Προδότης"),
            "intro_spy_mafia",
            Wait(5.0),
            "night_person_close",
            OverlayText("Σερίφης"),
            "night_cop_open",
            Choice(Sheriff),
            # Wait(5.0),
            "night_person_close",
            OverlayText("Τρέλα"),
            "intro_madness"
        ]

        # for k, v in Data.amount_roles.items():
        #     if v > 0:
        #         self.intro_stages = 

        self.index = 0
        self.clock_event = None
        self.timer_event = None


    def on_enter(self):
        Data.day += 1


        container = self.ids.players_container_night
        container.clear_widgets()
        
        # create and append the widgets dynamically
        self.player_item_list = []
        for player in Data.assigned_players:
            item = PlayerItem(
                player=player,
                screen=self,
                player_name=player.name,
                emoji=player.role.data["emoji"]
            )
            self.player_item_list.append(item)
            container.add_widget(item)

        self.stages = self.intro_stages if Data.current_state == GamePhase.FIRST_NIGHT else self.night_stages

        self.show_overlay()
        self.play_stage()


    def revealed(self, player):
        emoji = player.role.data['emoji']
        print(f"Emoji: {emoji} | Type: {type(emoji)} | Length: {len(emoji)}")
        self.change_text_overlay(f"Ο/Η {player.name} είναι [font=Twemoji]{emoji}[/font] {player.role.data["role"]}")
        self.show_overlay()
        self.timer_event = Clock.schedule_once(self.next_stage, 4)


    def show_overlay(self):
        if not self.overlay: # dynamic overlay creation
            from kivy.factory import Factory
            self.overlay = Factory.LoadingOverlay()
        
        # Open the overlay to lock controls and show the text
        if not self.overlay_open:
            self.overlay_open = True
            self.overlay.open()


    def change_text_overlay(self, new_text: str) -> None:
        if not self.overlay: # dynamic overlay creation
            from kivy.factory import Factory
            self.overlay = Factory.LoadingOverlay()
        
        # Open the overlay to lock controls and show the text
        self.overlay.overlay_text = new_text

    
    def stop_overlay(self):
        if not self.overlay: # dynamic overlay creation
            from kivy.factory import Factory
            self.overlay = Factory.LoadingOverlay()

        if self.overlay_open:
            self.overlay_open = False
            self.overlay.dismiss()      


    def timer_overlay(self, sec, dt=None):
        if not sec - 1 < 0:
            self.change_text_overlay(f"Χρόνος κοιτάγματος: {sec}")
            callback = partial(self.timer_overlay, sec - 1)
            self.timer_event = Clock.schedule_once(callback, 1) 
        else:
            self.change_text_overlay(f"Χρόνος κοιτάγματος: {sec}")
            self.next_stage()


    def choice(self, who: Role):
        for player_item in self.player_item_list:
            player_item.action_button_text = "Reveal" if who == Sheriff else "Kill"
            Data.night_action = True
            Data.night_action_role = who
            if player_item.player.role == Sheriff:
                player_item.bg_color = [0.7, 0.7, 0.7, 0.7]
                player_item.show_role_emoji = True
                player_item.action_button_text = "Known"


    def play_stage(self):
        if self.index >= len(self.stages):
            self.stop_overlay()
            Data.current_state = GamePhase.VOTING
            self.timer_event = Clock.schedule_once(self.next_screen, 1.5)
            return

        stage = self.stages[self.index]

        if type(stage) == Wait:
            callback = partial(self.timer_overlay, stage.sec)
            self.clock_event = Clock.schedule_once(callback, 0)    
            return
        elif type(stage) == Choice:
            self.stop_overlay()
            self.choice(stage.whos)
            return
        elif type(stage) == OverlayText:
            self.change_text_overlay(stage.msg)
            self.next_stage()
            return

        SoundManager.play_narration(stage)
        self.clock_event = Clock.schedule_once(self.next_stage, SoundManager.get_length(stage))


    def next_screen(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'day_voting_screen'


    def next_stage(self, dt=None):
        self.index += 1
        self.play_stage()


    def pause_narration(self):
        SoundManager.stop_narration()


    def resume_narration(self):
        SoundManager.continue_narration()


class LoadingOverlay(ModalView):
    overlay_text = StringProperty("Loading...") # Now root.text exists!
    screen_onj = ObjectProperty(None)