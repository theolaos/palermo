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
        # self.night_stages = [
        #     OverlayText("Νεα νύχτα"),
        #     "night_intro",
        #     OverlayText("Δολοφόνοι"),
        #     "night_start_mafia",
        #     "night_mafia_target",
        #     Choice(Killer),
        #     "night_people_close",
        #     ClearList(),
        #     OverlayText("Σερίφης"),
        #     "night_cop_open",
        #     Choice(Sheriff),
        #     ClearList(),
        #     "night_person_close",
        # ]

        # self.intro_stages = [
        #     OverlayText("Νεα νύχτα"),
        #     "night_intro",
        #     OverlayText("Δολοφόνοι"),
        #     "night_start_mafia",
        #     Wait(6.0),
        #     "night_people_close",
        #     OverlayText("Προδότης"),
        #     "intro_spy_mafia",
        #     Wait(5.0),
        #     "night_person_close",
        #     OverlayText("Σερίφης"),
        #     "night_cop_open",
        #     Choice(Sheriff),
        #     # Wait(5.0),
        #     "night_person_close",
        #     ClearList(),
        #     OverlayText("Τρέλα"),
        #     "intro_madness"
        # ]


        intro_stage_mapping = {
            Killer: [
                OverlayText("Δολοφόνοι"),
                "night_start_mafia",
                Wait(6.0),
                "night_people_close"
            ],
            Snitch: [
                OverlayText("Προδότης"),
                "intro_spy_mafia",
                Wait(5.0),
                "night_person_close"
            ],
            Crazy: [
                OverlayText("Τρέλα"),
                "intro_madness"
            ]
        }

        night_stage_mapping = {
            Killer: [
                OverlayText("Δολοφόνοι"),
                "night_start_mafia",
                "night_mafia_target",
                Choice(Killer),
                "night_people_close",
                ClearList()
            ],
            Sheriff: [
                OverlayText("Σερίφης"),
                "night_cop_open",
                Choice(Sheriff),
                "night_person_close",
                ClearList()
            ]
        }

        self.intro_stages = [
            OverlayText("Νεα νύχτα"),
            "night_intro"
        ]

        self.night_stages = [
            OverlayText("Νεα νύχτα"),
            "night_intro"
        ]

        for role, amount in Data.amount_roles.items():
            if amount > 0:
                # Dynamically build the Intro Stages
                if role in intro_stage_mapping:
                    self.intro_stages.extend(intro_stage_mapping[role])

                # Dynamically build the Night Stages
                if role in night_stage_mapping:
                    self.night_stages.extend(night_stage_mapping[role])

        print(self.intro_stages, self.night_stages)
        return self.intro_stages if Data.current_state == GamePhase.FIRST_NIGHT else self.night_stages

        # return self.night_stages

    def next_screen(self, dt=None):
        if Data.current_state == GamePhase.FIRST_NIGHT:
            Data.current_state = GamePhase.FIRST_VOTING
        elif Data.current_state == GamePhase.NIGHT:
            Data.current_state = GamePhase.VOTING
        else:
            print("Wrong game phase")
            Data.current_state = GamePhase.VOTING

        self.manager.transition.direction = 'left'
        self.manager.current = 'day_voting_screen'
