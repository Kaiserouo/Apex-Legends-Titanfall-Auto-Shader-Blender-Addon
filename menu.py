"""
    Main menu registering script
    Define menu in other python file and expose its menu_func and classes
    that needs registering
"""

import bpy
from .menu_apex import apex_menu_func, apex_classes
from .menu_titanfall import titanfall_menu_func, titanfall_classes

classes = (
    *apex_classes,
    *titanfall_classes
)

menu_funcs = (
    apex_menu_func,
    titanfall_menu_func
)

def register():
    for c in classes:
        if c != None:
            bpy.utils.register_class(c)
    for menu_func in menu_funcs:
        bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)
        bpy.types.VIEW3D_MT_pose_context_menu.append(menu_func)

def unregister():
    for menu_func in menu_funcs:
        bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
        bpy.types.VIEW3D_MT_pose_context_menu.remove(menu_func)
    for c in classes:
        if c != None:
            bpy.utils.unregister_class(c)