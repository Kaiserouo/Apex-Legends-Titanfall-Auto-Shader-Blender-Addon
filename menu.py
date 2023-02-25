from . import utils, config
import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty
from pathlib import Path

class ApexShadeActiveLegendOp(bpy.types.Operator):
    """Shade one active Apex Legend. Can select either mesh or armature. Only shades ONE object (the active one)."""
    bl_idname = "apexaddon.shade_active_legend"
    bl_label = "Shade Active Apex Legend"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        methods = {
            'MESH': utils.shadeMesh,
            'ARMATURE': utils.shadeArmature
        }
        if obj.type in methods:
            methods[obj.type](obj)
        else:
            raise Exception(f'{obj} is not one of the following: {list(methods.keys())}')
        return {'FINISHED'}

class ApexShadeSelectedLegendOp(bpy.types.Operator):
    """Shade all selected Apex Legends. Can select multiple meshes or armatures."""
    bl_idname = "apexaddon.shade_selected_legend"
    bl_label = "Shade Selected Apex Legend"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        methods = {
            'MESH': utils.shadeMesh,
            'ARMATURE': utils.shadeArmature
        }
        for i, obj in enumerate(context.selected_objects):
            print(f'[ShadeAll {i}/{len(context.selected_objects)}] {obj}')
            if obj.type in methods:
                methods[obj.type](obj, do_check=False)
            else:
                raise Exception(f'{obj} is not one of the following: {list(methods.keys())}')
        return {'FINISHED'}
        
class ApexShadeSelectedLegendWithoutOpacityOp(bpy.types.Operator):
    """Shade all selected Apex Legends, but don't use opacity multiplier"""
    bl_idname = "apexaddon.shade_selected_legend_without_opacity"
    bl_label = "Shade Selected Apex Legend (Without Opacity Multiplier)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        methods = {
            'MESH': utils.shadeMesh,
            'ARMATURE': utils.shadeArmature
        }
        for i, obj in enumerate(context.selected_objects):
            print(f'[ShadeAllWithoutOpacity {i}/{len(context.selected_objects)}] {obj}')
            if obj.type in methods:
                methods[obj.type](obj, do_check=False, node_adder_cls=utils.NodeAdderWithoutOpacity)
            else:
                raise Exception(f'{obj} is not one of the following: {list(methods.keys())}')
        return {'FINISHED'}

class ApexImportCASOp(bpy.types.Operator, ImportHelper):
    """Operator for setting Core Apex Shader blender file path."""

    bl_idname = "apexaddon.set_cas_blend_file_path"
    bl_label = "Set Core Apex Shader blender file path"

    filename_ext = ".blend"
    use_filter_folder = True

    def execute(self, context):
        filepath = self.properties.filepath
        config.CORE_APEX_SHADER_BLENDER_FILE = filepath

        return{'FINISHED'}

# https://blender.stackexchange.com/questions/14738/use-filemanager-to-select-directory-instead-of-file
# note we are > 2.8
class ApexImportRecolor(bpy.types.Operator):
    """Import recolor"""
    bl_idname = "apexaddon.import_recolor"
    bl_label = "Import Recolor"
    bl_options = {'REGISTER'}
    directory: bpy.props.StringProperty(name="Directory", options={"HIDDEN"})
    filter_folder: bpy.props.BoolProperty(default=True, options={"HIDDEN"})

    def execute(self, context):
        # chosen dir: `self.directory`
        print("[ImportRecolor] Selected dir: '" + self.directory + "'")

        obj = context.active_object
        methods = {
            'MESH': utils.recolorMesh,
            'ARMATURE': utils.recolorArmature
        }
        if obj.type in methods:
            methods[obj.type](obj, Path(self.directory))
        else:
            raise Exception(f'{obj} is not one of the following: {list(methods.keys())}')
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def makeRemoveTextureSelectedClass(texture_type):
    # NOTE: when registering class, bl_idname must only contain lower case w/o special chars
    # texture_type.lower() may not be enough
    class ApexRemoveTextureSelectedOp(bpy.types.Operator):
        # f"""Remove texture '{texture_type}' from all selected armature or mesh"""
        bl_idname = f"apexaddon.remove_texture_{texture_type.lower()}"
        bl_label = f"Remove {texture_type}"
        bl_options = {'REGISTER', 'UNDO'}

        def execute(self, context):
            methods = {
                'MESH': utils.removeTextureMesh,
                'ARMATURE': utils.removeTextureArmature
            }
            for i, obj in enumerate(context.selected_objects):
                print(f'[RemoveAllTexture {texture_type} {i}/{len(context.selected_objects)}] {obj}')
                if obj.type in methods:
                    methods[obj.type](obj, texture_type)
                else:
                    raise Exception(f'{obj} is not one of the following: {list(methods.keys())}')
            return {'FINISHED'}
    
    # in-class docstring cannot be f-string, or it will become None, so we set it here
    # a bit hacky but it works...
    ApexRemoveTextureSelectedOp.__doc__ = f"Remove texture '{texture_type}' from all selected armature or mesh"

    return ApexRemoveTextureSelectedOp

removable_texture_ls = [
    'albedoTexture',
    'aoTexture',
    'cavityTexture',
    'emissiveTexture',
    'glossTexture',
    'normalTexture',
    'specTexture',
    'opacityMultiplyTexture',
    'scatterThicknessTexture',
]

remove_texture_class_ls = [
    makeRemoveTextureSelectedClass(texture_type) 
    for texture_type in removable_texture_ls
]

class ApexRemoveTextureSubmenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_apex_remove_texture_submenu"
    bl_label = "Remove Texture From Selected Legends"

    def draw(self, context):
        layout = self.layout
        for rm_cls in remove_texture_class_ls:
            layout.operator(rm_cls.bl_idname)

# ---
# class contains everything that is not a submenu
# used for (un)registering
classes = (
    ApexShadeActiveLegendOp,
    ApexShadeSelectedLegendOp,
    ApexShadeSelectedLegendWithoutOpacityOp,
    *remove_texture_class_ls,
    ApexRemoveTextureSubmenu,
    ApexImportRecolor,
    ApexImportCASOp
)

class Submenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_apex_shade_submenu"
    bl_label = "Apex Shader"

    def draw(self, context):
        layout = self.layout
        layout.operator(ApexShadeActiveLegendOp.bl_idname)
        layout.operator(ApexShadeSelectedLegendOp.bl_idname)
        layout.operator(ApexShadeSelectedLegendWithoutOpacityOp.bl_idname)
        layout.menu(ApexRemoveTextureSubmenu.bl_idname)
        layout.operator(ApexImportRecolor.bl_idname)
        layout.operator(ApexImportCASOp.bl_idname)


def menu_func(self, context):
    layout = self.layout
    layout.menu(Submenu.bl_idname)

def register():
    for c in classes:
        if c != None:
            bpy.utils.register_class(c)
    bpy.utils.register_class(Submenu)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)
    bpy.types.VIEW3D_MT_pose_context_menu.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(menu_func)
    bpy.utils.unregister_class(Submenu)
    for c in classes:
        if c != None:
            bpy.utils.unregister_class(c)