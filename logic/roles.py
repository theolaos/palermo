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

from .exceptions import TooManyRoles, UnBalanced, NotEnoughRoles

# @dataclass
# class Player:
#     votes: int
class Role: ...


class Town(Role): ...
class Mafia(Role): ...


class Citizen(Town):
    data = {
        "emoji" : "👨‍🦱",
        "role" : "Πολίτης",
        "short" : "Ένας απλός κάτοικος της πόλης.",
        "long" : "Δεν έχεις ειδικές δυνάμεις τη νύχτα, αλλά η ψήφος σου την ημέρα είναι καθοριστική για να βρεθούν οι ένοχοι."
    }

class Mayor(Town):
    data = {
        "emoji" : "🤵",
        "role" : "Δήμαρχος",
        "short" : "Ο ηγέτης της πόλης.",
        "long" : "Μπορείς να αποκαλύψεις την ταυτότητά σου δημόσια. Όταν το κάνεις, η ψήφος σου μετράει διπλή στις ψηφοφορίες."
    }

class Sheriff(Town):
    data = {
        "emoji": "👮",
        "role": "Αστυνομικός",
        "short": "Ο προστάτης του νόμου.",
        "long": "Κάθε νύχτα μπορείς να ανακρίνεις έναν παίκτη για να μάθεις αν ανήκει στη Μαφία ή αν είναι αθώος."
    }


class Killer(Mafia):
    data = {
        "emoji": "🔪",
        "role": "Δολοφόνος",
        "short": "Το εκτελεστικό όργανο του εγκλήματος.",
        "long": "Κάθε νύχτα επιλέγεις έναν στόχο μαζί με την υπόλοιπη Μαφία για να τον βγάλετε από το παιχνίδι."
    }


class Snitch(Mafia):
    data = {
        "emoji": "🤝",
        "role": "Προδότης",
        "short": "Ο προδότης του χωριού.",
        "long": "Γνωρίζεις ποιοι είναι οι δολοφόνοι και άμα χρειαστεί παίρνεις εσύ την ήττα ώστε να επιτύχουν οι δολοφόνοι."
    }


class Crazy(Mafia):
    data = {
        "emoji": "🧙",
        "role": "Τρέλα",
        "short": "Ο παίκτης που θέλει να καταδικαστεί.",
        "long": "Ο στόχος σου είναι να κάνεις τους άλλους να σε υποψιαστούν και να σε ψηφίσουν για να σε βγάλουν από το παιχνίδι. Αν σε ψηφίσουν, κερδίζεις!"
    }

@dataclass
class Player:
    name: str
    role: Role
    vote: int = 0
    alive: bool = True
    phone_type: str = "Generic Phone"

class Data:
    players = 4
    day = 0
    amount_roles = {
        Citizen : 0,
        Mayor : 0,
        Sheriff : 0,
        Killer : 0,
        Snitch : 0,
        Crazy : 0
    }
    generated_roles = False
    pre_assign_roles = []
    assigned_roles = {}
    assigned_players: list[Player] = []
    current_state = None

    night_action = False


class Settings:
    ...


roles_list = [k for k, _  in Data.amount_roles.items()] 

def default_role_dict(
        players: int,
        amount_roles: dict[Role, int]
    ) -> None:
    
    for role, _ in Data.amount_roles.items():
        Data.amount_roles[role] = 0

    mafia = 0
    if players < 5:
        mafia = 1
    elif players < 10:
        mafia = 2
    else:
        mafia = int(players*0.17)

    sheriff = 1 if players < 10 else int(players*0.15)

    amount_roles.update({Killer : mafia})
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
    items = [(k, v) for k, v in amount_roles.items()]
    s = 0
    for role, item in items:
        s += item

    s_mafia = amount_roles[Killer]
    
    if s > players:
        raise TooManyRoles(f"Registered Players: {players}, Role Players: {s}")

    if s_mafia > players*0.5:
        raise UnBalanced(f"Registered Players: {players}, Role Killers: {s_mafia}")


def enough_roles(players, amount_roles) -> None:
    """
    Are there enough roles?

    THROWS: NotEnoughRoles()
    """
    items = [(k, v) for k, v in amount_roles.items()]
    s = 0
    for role, item in items:
        s += item

    if s < players:
        raise NotEnoughRoles(f"Registered Players: {players}, Role Players: {s}")


def add_citizens(players, amount_roles) -> None:
    """
    Adds Citizens to the roles, because there were not enough.
    """
    items = [(k, v) for k, v in amount_roles.items()]
    s = 0
    for role, item in items:
        s += item

    amount_roles[Citizen] += players - s 


def generate_pre_assign_roles_list(
        amount_roles: dict[Role, int],
        rng=None,
    ) -> list[Role]:
    role_list = []
    for k, v in amount_roles.items():
        role_list.extend([k] * v)

    rand = rng or random
    rand.shuffle(role_list)

    return role_list


def assign_roles(
        players_name: list,
        pre_assign_roles_list: list,
    ) -> dict[str, Role]:
    """
    Assign the roles at random to the players
    """
    return dict(zip(players_name, pre_assign_roles_list))
