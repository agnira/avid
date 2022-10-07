# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "avid",
    "author" : "Agni Rakai Sahakarya",
    "description" : "Addon to help edit video with blender",
    "blender" : (3, 3, 0),
    "version" : (0, 0, 1),
    "location" : "Video Sequencer > Properties > Avid",
    "category" : "Sequencer",
}

if "bpy" in locals():
    import imp
    imp.reload(ui_operator)
    imp.reload(ui)
else:
    from . import ui, ui_operator

import bpy

def register():
    ui_operator.register()
    ui.register()
    pass

def unregister():
    ui_operator.unregister()
    ui.unregister()
    pass

if __name__ == "__main__":
    register()