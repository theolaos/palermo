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

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty

class RoleSelectionScreen(Screen): ...

class RoleItem(BoxLayout):
    # Properties that can be passed from KV or updated dynamically
    count = NumericProperty(0)
    role_name = StringProperty("")
    short_desc = StringProperty("")
    long_desc = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_expanded = False

    def toggle_expand(self, touch):
        # Check if the touch actually happened inside this specific widget
        if self.collide_point(*touch.pos):
            # If the user clicked the step buttons, don't expand/collapse
            if self.ids.minus_btn.collide_point(*touch.pos) or self.ids.plus_btn.collide_point(*touch.pos):
                return
            
            # Toggle the expansion state
            if not self.is_expanded:
                self.height = 180  # Expanded height
                self.ids.extra_desc.text = self.long_desc
                self.is_expanded = True
            else:
                self.height = 80   # Collapsed height
                self.ids.extra_desc.text = ""
                self.is_expanded = False

    def increment(self):
        self.count += 1

    def decrement(self):
        if self.count > 0:
            self.count -= 1