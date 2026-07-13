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

from .exceptions import TooManyRoles, UnBalanced

# @dataclass
# class Player:
#     votes: int
class Role: ...


class Town(Role): ...
class Mafia(Role): ...


class Citizen(Town):
    data = {
        "emoji" : "👤",
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
        "role": "Ρουφιάνος",
        "short": "Το εκτελεστικό όργανο του εγκλήματος.",
        "long": "Κάθε νύχτα επιλέγεις έναν στόχο μαζί με την υπόλοιπη Μαφία για να τον βγάλετε από το παιχνίδι."
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
    alive: bool = True
    phone_type: str = "Generic Phone"

class Data:
    players = 4
    amount_roles = {
        Citizen : 0,
        Mayor : 0,
        Sheriff : 0,
        Killer : 0,
        Snitch : 0,
        Crazy : 0
    }

roles_list = [k for k, _  in Data.amount_roles.items()] 

def default_role_dict(
        players: int,
        amount_roles: dict[Role, int]
    ) -> None:
    
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