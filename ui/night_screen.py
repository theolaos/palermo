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

from .game_loop import GameLoop


# import os
# print("Font path exists:", os.path.exists("ui/fonts/twemoji.ttf"))

class NightScreen(GameLoop):
    def choose_stage(self):
        self.night_stages = [
            OverlayText("Νεα νύχτα"),
            "night_intro",
            OverlayText("Δολοφόνοι"),
            "night_start_mafia",
            "night_mafia_target",
            Choice(Killer),
            "night_people_close",
            OverlayText("Σερίφης"),
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

        # return self.intro_stages if Data.current_state == GamePhase.FIRST_NIGHT else self.night_stages
        return self.night_stages
