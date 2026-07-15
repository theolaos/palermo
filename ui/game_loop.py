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

import random

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
        if Data.current_state in [GamePhase.FIRST_NIGHT, GamePhase.NIGHT, GamePhase.VOTING] and Data.night_action:
            print(Data.night_action_role, self.player, Data.dead_players)
            if self.player in Data.dead_players:
                return

            elif Data.night_action_role == Sheriff:
                if self.player.role == Sheriff:
                    return

                self.action_button_text = "Revealed"
                self.show_role_emoji = Data.night_action_role == Sheriff 

                Data.night_action = False

                self.screen.revealed(self.player)
            elif Data.night_action_role == Killer:
                self.action_button_text = "Killed"
                self.default_emoji = "💀"
                self.bg_color = [0.7, 0.7, 0.7, 0.7]

                self.player.alive = False

                Data.night_action = False
                
                self.screen.killed(self.player)
            
        else:
            self.player.vote += 1


class GameLoop(Screen):
    bottom_button = StringProperty("PAUSE")
    bottom_bg_color = ListProperty((0.2, 0.8, 0.4, 1))
    current_text = StringProperty("Μια νέα Νύχτα στο Παλέρμο")

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.introductory_night = False # turns to True if it happened.


        self.stages = None

        self.index = 0
        self.clock_event = None
        self.timer_event = None


    def on_enter(self):
        Data.day += 1
        self.index = 0
        self.clock_event = None
        self.timer_event = None

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

        self.dead_player_item_list = []
        for player in Data.dead_players:
            item = PlayerItem(
                player=player,
                screen=self,
                player_name=player.name,
                emoji="💀"
            )
            item.action_button_text = "Dead"
            item.bg_color =[0.7, 0.7, 0.7, 0.7]
            item.show_role_emoji = True
            item.default_emoji = "💀"
            self.dead_player_item_list.append(item)
            container.add_widget(item)            

        self.stages = self.choose_stage()
        

        self.show_overlay()
        self.play_stage()
    

    def choose_stage(self): 
        print("not implemented")


    def revealed(self, player):
        emoji = player.role.data['emoji']
        print(f"Emoji: {emoji} | Type: {type(emoji)} | Length: {len(emoji)}")
        self.change_text_overlay(f"Ο/Η {player.name} είναι [font=ui/fonts/twemoji]{emoji}[/font] {player.role.data["role"]}")
        self.show_overlay()
        self.timer_event = Clock.schedule_once(self.next_stage, 4)


    def killed(self, player):
        emoji = player.role.data['emoji']
        print(f"Emoji: {emoji} | Type: {type(emoji)} | Length: {len(emoji)}")
        self.change_text_overlay(f"Ο/Η {player.name} σκωτώθηκε [font=ui/fonts/twemoji]💀[/font].")
        self.show_overlay()
        self.timer_event = Clock.schedule_once(self.next_stage, 2)


    def show_overlay(self):
        if not Data.overlay: # dynamic overlay creation
            from kivy.factory import Factory
            Data.overlay = Factory.LoadingOverlay()
        
        # Open the overlay to lock controls and show the text
        if not Data.overlay_open:
            Data.overlay_open = True
            Data.overlay.open()


    def change_text_overlay(self, new_text: str) -> None:
        if not Data.overlay: # dynamic overlay creation
            from kivy.factory import Factory
            Data.overlay = Factory.LoadingOverlay()
        
        # Open the overlay to lock controls and show the text
        Data.overlay.overlay_text = new_text

    
    def stop_overlay(self):
        if not Data.overlay: # dynamic overlay creation
            from kivy.factory import Factory
            Data.overlay = Factory.LoadingOverlay()

        if Data.overlay_open:
            Data.overlay_open = False
            Data.overlay.dismiss()      


    def timer_overlay(self, dt, sec, msg="Χρόνος κοιτάγματος:"):
        if not sec - 1 < 0:
            print("Showing timer overlay")
            self.change_text_overlay(f"{msg} {sec}")
            self.show_overlay()
            callback = partial(self.timer_overlay, sec - 1, msg)
            self.timer_event = Clock.schedule_once(callback, 1) 
        else:
            self.change_text_overlay(f"{msg} {sec}")
            self.next_stage()


    def choice(self, who: Role):
        if who == Sheriff:
            for player in Data.dead_players:
                if player.role == Sheriff:
                    print("Random timer, because sheriff died")
                    callback = partial(self.timer_overlay, random.uniform(5.3, 10.3), "Περίμενε")
                    self.clock_event = Clock.schedule_once(callback, 0)      
                    return 

        
        for player_item in self.player_item_list:
            print("before", player_item.action_button_text, who)

            player_item.action_button_text = "Reveal" if who == Sheriff else "Kill"
            
            print("after",player_item.action_button_text, who)

            Data.night_action = True
            Data.night_action_role = who

            if player_item.player.role == Sheriff and who == Sheriff:
                print("Change Sheriff emoji", player_item.emoji)
                player_item.bg_color = [0.7, 0.7, 0.7, 0.7]
                player_item.show_role_emoji = True
                player_item.action_button_text = "Known"

            elif player_item.player.role == Killer and who == Killer:
                print("Change cop emoji")
                player_item.bg_color = [0.7, 0.7, 0.7, 0.7]
                player_item.show_role_emoji = True
                player_item.action_button_text = "Known"
            
            if not player_item.player.alive:
                if who == Sheriff:
                    player_item.show_role_emoji = True
                player_item.default_emoji = "💀"


    def clear_list(self):
        print("cleared")
        for player_item in self.player_item_list:
            print("cleared:", player_item)
            player_item.action_button_text = "Action"
            player_item.bg_color = [1, 1, 1, 1]
            player_item.show_role_emoji = False


    def play_stage(self):
        print("play_stage index", self.stages[self.index] if self.index < len(self.stages) else "length")

        if self.index >= len(self.stages):
            self.stop_overlay()
            dead_this_round = [p for p in Data.assigned_players if not p.alive]
            Data.dead_players.extend(dead_this_round)

            Data.assigned_players = [p for p in Data.assigned_players if p.alive]

            self.timer_event = Clock.schedule_once(self.next_screen, 0.7)
            return

        stage = self.stages[self.index]

        if type(stage) == Wait:
            params = [stage.sec]
            if stage.msg:
                params.append(stage.msg)

            callback = partial(self.timer_overlay, *params)
            self.clock_event = Clock.schedule_once(callback, 0)    
            return
        elif type(stage) == Choice:
            self.stop_overlay()
            print("stopped overlay")
            self.choice(stage.whos)
            return
        elif type(stage) == OverlayText:
            self.change_text_overlay(stage.msg)
            self.next_stage()
            return
        elif type(stage) == ClearList:
            print("ran clear list")
            self.clear_list()
            self.next_stage()
            return

        SoundManager.play_narration(stage)
        self.clock_event = Clock.schedule_once(self.next_stage, SoundManager.get_length(stage))


    def next_screen(self, dt=None):
        self.manager.transition.direction = 'left'
        self.manager.current = 'day_voting_screen'


    def next_stage(self, dt=None):
        self.index += 1
        print("next_stage index", self.stages[self.index] if self.index < len(self.stages) else "length")
        self.play_stage()


    def pause_narration(self):
        SoundManager.stop_narration()


    def resume_narration(self):
        SoundManager.continue_narration()


class LoadingOverlay(ModalView):
    overlay_text = StringProperty("Loading...") # Now root.text exists!
    screen_onj = ObjectProperty(None)