bl_info = {
    "name": "Apex Legends Auto Shader Addon",
    "description": "Addon that helps shading Apex Legends characters.",
    "author": "Kaiserouo",
    "version": (1, 1),
    "blender": (3, 2, 0),
    "location": "View3D > Object Context Menu / Pose Context Menu > Apex Auto Shader",
    "doc_url": "https://github.com/Kaiserouo/Apex-Legends-Auto-Shader-Blender-Addon",
    "category": "Object"
}

import bpy
from . import menu

def register():
    menu.register()
    
def unregister():
    menu.unregister()

if __name__ == "__main__":
    register()