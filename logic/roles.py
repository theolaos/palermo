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

from dataclasses import dataclass

from .exceptions import TooManyRoles

# @dataclass
# class Player:
#     votes: int
class Role: ...


class Allies(Role): ...


class Citizen(Allies): ...


class Mayor(Allies): ...


class Sheriff(Allies): ...


class Enemies(Role): ...


class Mafia(Enemies): ...


class Crazy(Enemies): ...


@dataclass
class Player:
    name: str
    role: Role
    alive: bool = True
    phone_type: str = "Generic Phone"


amount_roles = {
    Citizen : 0,
    Mayor : 0,
    Sheriff : 0,
    Mafia : 0,
    Crazy : 0
}


def default_role_dict(
        players: int,
        amount_roles: dict[Role, int]
    ) -> None:
    
    mafia = 2 if players < 10 else int(players*0.2)
    sheriff = 1 if players < 10 else int(players*0.15)

    amount_roles.update({Mafia : mafia})
    amount_roles.update({Sheriff : sheriff})
    amount_roles.update({Citizen : players - mafia - sheriff})


def verify_role_dict(
        players: int,
        amount_roles: dict[Role, int]
    ) -> None:
    """
    Verifies if the amount of roles are correct, and there are no imbalances.
    
    THROWS: TooManyRoles() or UnBalanced()
    """
    items = [(k, v) for k, v in d.items()]
    s = 0
    for role, item in items:
        s += item

    s_mafia = amount_roles[Mafia]
    
    if item > players:
        raise TooManyRoles()

    if s_mafia > players*0.5:
        raise UnBalanced()


def assign_roles(
        players_name: list,
        amount_roles: dict[Role, int],
        rng=None,
    ) -> dict[str, Role]:
    """
    Assign the roles at random to the players
    """

    # Assuming that the amount_roles are verified
    role_list = []

    for k, v in d.items():
        role_list.extend([k]*v)

    rand = rng or random

    rand.shuffle(role_list)

    return dict(zip(players_name, role_list))