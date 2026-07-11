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

from kivy.config import Config

# Set the window width and height to match a standard phone aspect ratio (e.g., 360x640)
scalar = 1.5
Config.set('graphics', 'width', str(int(340*scalar)))
Config.set('graphics', 'height', str(int(640*scalar)))
Config.set('graphics', 'resizable', False)


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager

from ui.main_menu_screen import MainMenuScreen
from ui.role_selection_screen import RoleSelectionScreen
from ui.input_players_amount_screen import InputPlayersAmountScreen


class GameScreenManager(ScreenManager): ...

class MobileApp(App):
    def build(self):
        return GameScreenManager()


if __name__ == "__main__":
    MobileApp().run()