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

class DayVotingScreen(GameLoop):
    def choose_stage(self):

        
        self.day_stages = [
            Wait(5, "Μια μέρα ξημερώνει στο Παλέρμο. Μπορείτε να ανοίξετε τα μάτια σας."),
            Wait(3, "Η ψηφοφορία έχει ξεκινήσει."),
            Voting(),
            Wait(3, "Η ψηφοφορία έχει τελειώσει."),
        ]

        self.intro_stages = self.night_stages.append(
            Wait(6, "Το άτομο το οποίο ψηφίσατε εκτός παιχνιδιού να πάρει το κινητό στην θέση του.")
        )


        return self.intro_stages if Data.current_state == GamePhase.FIRST_VOTING else self.day_stages

    def next_screen(self, dt=None):
        if Data.current_state in [GamePhase.FIRST_VOTING, GamePhase.VOTING]:
            Data.current_state = GamePhase.NIGHT
        else:
            print("Wrong game phase")
            Data.current_state = GamePhase.NIGHT

        self.manager.transition.direction = 'left'
        self.manager.current = 'night_screen'