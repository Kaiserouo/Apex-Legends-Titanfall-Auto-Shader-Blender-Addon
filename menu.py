from . import utils, config
import bpy
from bpy_extras.io_utils import ImportHelper

class ApexShadeLegendOp(bpy.types.Operator):
    """Shade Selected Apex Legend. Can select either mesh or armature."""
    bl_idname = "apexaddon.shade_legend"
    bl_label = "Shade Selected Apex Legend"
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
            raise Exception(f'Not one of the following: {list(methods.keys())}')
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


# ---
# class contains everything that is not a submenu
# used for (un)registering
classes = (
    ApexShadeLegendOp,
    ApexImportCASOp
)

class Submenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_apex_shade_submenu"
    bl_label = "Apex Shader"

    def draw(self, context):
        layout = self.layout
        layout.operator(ApexShadeLegendOp.bl_idname)
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