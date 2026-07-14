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

from kivy.core.audio import SoundLoader

directory = "script/narration/"

class SoundManager:
    narr = {
        "intro_madness": SoundLoader.load(directory + "night/intro_madness.wav"),
        "intro_spy_mafia": SoundLoader.load(directory + "night/intro_spy_mafia.wav"),

        "night_intro": SoundLoader.load(directory + "night/night_intro.wav"),
        "night_start_mafia": SoundLoader.load(directory + "night/night_start_mafia.wav"),
        "night_mafia_target": SoundLoader.load(directory + "night/night_mafia_target.wav"),
        "night_people_close": SoundLoader.load(directory + "night/night_mafia_close.wav"),
        "night_cop_open": SoundLoader.load(directory + "night/night_cop_open.wav"),
        "night_person_close": SoundLoader.load(directory + "night/night_cop_close.wav"),

        "day_start": SoundLoader.load(directory + "day/day_start.wav"),
        "day_voting_start": SoundLoader.load(directory + "day/day_voting_start.wav"),
        "day_voting_end": SoundLoader.load(directory + "day/day_voting_end.wav"),
        "first_day_elimination": SoundLoader.load(directory + "day/first_day_elimination.wav"),
 
        "win_mafia": SoundLoader.load(directory + "win/win_mafia.wav"),
        "win_madness": SoundLoader.load(directory + "win/win_madness.wav"),
        "win_village": SoundLoader.load(directory + "win/win_village.wav"),

        # "death_option1": SoundLoader.load(directory + "deaths/death_option1.wav"),
        # "death_option2": SoundLoader.load(directory + "deaths/death_option2.wav"),
        # "death_option3": SoundLoader.load(directory + "deaths/death_option3.wav"),
        "death_none": SoundLoader.load(directory + "deaths/death_none.wav"),
    }

    last_narration = [None, None]

    @staticmethod
    def change_volume(new_volume: float) -> None:
        """
        Volume should be between 0 and 1
        """
        for _, v in SoundManager.narr.items():
            v.volume = new_volume
        
        
    @staticmethod
    def play_narration(name_narration: str) -> None:
        SoundManager.narr[name_narration].play()
        SoundManager.last_narration = [name_narration, 0]


    @staticmethod
    def stop_narration(name_narration: str) -> None:
        sound = SoundManager.narr[name_narration]
        sound.stop()
        t = sound.get_pos()
        SoundManager.last_narration = [name_narration, t]


    @staticmethod
    def continue_narration(name_narration: str) -> None:
        sound = SoundManager.narr[name_narration]
        sound.play()
        sound.seek(SoundManager.last_narration[1])
        SoundManager.last_narration = [name_narration, t]

    @staticmethod
    def get_length(name_narration: str) -> float:
        return SoundManager.narr[name_narration].length
