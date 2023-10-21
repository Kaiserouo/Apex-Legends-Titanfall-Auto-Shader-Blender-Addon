"""
    Titanfall shader menu
"""

from . import utils, config
import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty
from pathlib import Path
from .node_adder import *

CURRENT_NODEADDER = TitanfallSGNodeAdder

# https://blender.stackexchange.com/questions/14738/use-filemanager-to-select-directory-instead-of-file
# note we are > 2.8
class TitanfallShadeActiveMaterialOp(bpy.types.Operator):
    """Shade active material by choosing folder"""
    bl_idname = "apexaddon.titanfall_shade_active"
    bl_label = "Shade Active Material (Folder)"
    bl_options = {'REGISTER'}
    directory: bpy.props.StringProperty(name="Directory", options={"HIDDEN"})
    filter_folder: bpy.props.BoolProperty(default=True, options={"HIDDEN"})

    def execute(self, context):
        # chosen dir: `self.directory`
        print("[TitanfallShadeActiveMaterial] Selected dir: '" + self.directory + "'")

        obj = context.active_object
        if obj.type != 'MESH':
            raise Exception(f'{obj} is not mesh')
        
        # note that we don't use utils.recolorMesh because it creates new material
        # but shadeMesh requires the active material have 1 image texture
        # we clear material and add random image
        mat = obj.active_material
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()

        img_path = next(Path(self.directory).iterdir())
        img_node = nodes.new(type='ShaderNodeTexImage')
        img_node.image = bpy.data.images.load(str(img_path))

        # do shading
        utils.shadeMesh(obj, CURRENT_NODEADDER)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# ---

class TitanfallSubmenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_titanfall_shade_submenu"
    bl_label = "Titanfall Shader"

    def draw(self, context):
        layout = self.layout
        layout.operator(TitanfallShadeActiveMaterialOp.bl_idname)

# class contains everything that needs (un)registering
titanfall_classes = (
    TitanfallShadeActiveMaterialOp,
    TitanfallSubmenu
)

def titanfall_menu_func(self, context):
    layout = self.layout
    layout.menu(TitanfallSubmenu.bl_idname)