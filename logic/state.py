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

from enum import Enum, auto
from dataclasses import dataclass

from .roles import Role, Player


class GamePhase(Enum):
    LOBBY = auto()
    FIRST_NIGHT = auto()
    NIGHT = auto()
    # DAY_DISCUSSION = auto()
    VOTING = auto()
    GAME_OVER = auto()

@dataclass
class Wait:
    sec: float


@dataclass
class Choice:
    whos: Role


def create_player_dataclass_list(d: dict[str, Role]) -> list[Player]:
    return [Player(k, v) for k, v in d.items()]

