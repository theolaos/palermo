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

from dataclasses import dataclass

# @dataclass
# class Player:
#     votes: int

class Allies: ...


class Citizen(Allies): ...


class Mayor(Allies): ...


class Sheriff(Allies): ...


class Enemies: ...


class Mafia(Enemies): ...


class Crazy(Enemies): ...


amount_roles = {
    Citizen : 0,
    Mayor : 0,
    Sheriff : 0,
    Mafia : 0,
    Crazy : 0
}


def create_role_dict(
        players: int,
        amount_roles: dict[Allies | Enemies, int]
    ) -> dict[Allies | Enemies, int]:
    """
    Calculates if the amount roles are correct, and there are no imbalances.
    """


def assign_roles(
        players_name: list[str],
        amount_roles: dict[Allies | Enemies, int],
    ) -> dict[str, Allies | Enemies]:
    """
    Assign the roles at random to the players
    """
