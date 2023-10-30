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
        
        utils.shadeMaterialByDirectory(obj.active_material, Path(self.directory), CURRENT_NODEADDER)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class TitanfallShadeByMaterialMatchingOp(bpy.types.Operator):
    "Choose a folder, try to match the name of subfolder for each material "
    "and shade from the most similarly names subfolder. "
    "Some matching may be wrong, especially if the material and subfolder doesn't have the same name"

    bl_idname = "apexaddon.titanfall_shade_material_matching"
    bl_label = "Shade By Material Name Matching (Folder)"
    bl_options = {'REGISTER'}
    directory: bpy.props.StringProperty(name="Directory", options={"HIDDEN"})
    filter_folder: bpy.props.BoolProperty(default=True, options={"HIDDEN"})

    def execute(self, context):
        # chosen dir: `self.directory`
        print("[TitanfallShadeMeshByMaterialMatching] Selected dir: '" + self.directory + "'")

        obj = context.active_object

        # get all meshes need shading
        if obj.type == 'MESH':
            meshes = [obj]
        elif obj.type == 'ARMATURE':
            meshes = [m for m in obj.children if m.type == 'MESH']
        else:
            raise Exception('Object is not mesh or armature')
        
        # get all materials needs shading 
        mat_ls = [mat for mesh in meshes for mat in mesh.data.materials]
        mat_ls = list(set(mat_ls))  # avoid shading same material multiple times

        # match name of material to folder
        mat_name_ls = [mat.name for mat in mat_ls]
        folder_name_ls = [p.name for p in Path(self.directory).iterdir() if p.is_dir()]
        name_map = utils.matchString(mat_name_ls, folder_name_ls)
        
        print('    Matching result:')
        for mat in mat_ls:
            print(f'        {mat.name} -> {name_map[mat.name]}')

        # shade all material
        for mat in mat_ls:
            mat_dir_path = Path(self.directory) / name_map[mat.name]
            utils.shadeMaterialByDirectory(mat, mat_dir_path, CURRENT_NODEADDER)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class TitanfallToggleEmissionOnOp(bpy.types.Operator):
    """Turn Emission Mix Node To Fac = 1"""
    bl_idname = "apexaddon.titanfall_emission_node_fac_one"
    bl_label = "Toggle Emission On"
    bl_options = {'REGISTER'}

    def execute(self, context):
        # chosen dir: `self.directory`
        print("[TitanfallShadeActiveMaterial] Selected dir: '" + self.directory + "'")

        obj = context.active_object

        # get all meshes need shading
        if obj.type == 'MESH':
            meshes = [obj]
        elif obj.type == 'ARMATURE':
            meshes = [m for m in obj.children if m.type == 'MESH']
        else:
            raise Exception('Object is not mesh or armature')
        
        mat_ls = [mat for mesh in meshes for mat in mesh.data.materials]

        for mat in mat_ls:
            for node in mat.node_tree.nodes:
                if node.label == 'Emission Mix Node':
                    node.inputs['Fac'].default_value = 1


        return {'FINISHED'}

# ---

class TitanfallSubmenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_titanfall_shade_submenu"
    bl_label = "Titanfall Shader"

    def draw(self, context):
        layout = self.layout
        layout.operator(TitanfallShadeActiveMaterialOp.bl_idname)
        layout.operator(TitanfallShadeByMaterialMatchingOp.bl_idname)

# class contains everything that needs (un)registering
titanfall_classes = (
    TitanfallShadeActiveMaterialOp,
    TitanfallShadeByMaterialMatchingOp,
    TitanfallSubmenu
)

def titanfall_menu_func(self, context):
    layout = self.layout
    layout.menu(TitanfallSubmenu.bl_idname)