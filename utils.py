
"""
>>> bpy.context.active_object
bpy.data.objects['pilot_medium_bloodhound_season_06_heist_LOD0_SEModelMesh.029']

>>> bpy.context.active_object.active_material
bpy.data.materials['bloodhound_lgnd_v20_boosted_body']

>>> nodes = bpy.data.materials['bloodhound_lgnd_v20_boosted_body'].node_tree.nodes
>>> nodes.items()
[('Material Output', bpy.data.materials['bloodhound_lgnd_v20_boosted_body'].node_tree.nodes["Material Output"]), ('Image Texture.001', bpy.data.materials['bloodhound_lgnd_v20_boosted_body'].node_tree.nodes["Image Texture.001"]), ('Image Texture.002', bpy.data.materials['bloodhound_lgnd_v20_boosted_body'].node_tree.nodes["Image Texture.002"]), ('Image Texture.005', bpy.data.materials['bloodhound_lgnd_v20_boosted_body'].node_tree.nodes["Image Texture.005"]), ('Image Texture.004', bpy.data.materials['bloodhound_lgnd_v20_boosted_body'].node_tree.nodes["Image Texture.004"]), ('Image Texture', bpy.data.materials['bloodhound_lgnd_v20_boosted_body'].node_tree.nodes["Image Texture"]), ('Image Texture.003', bpy.data.materials['bloodhound_lgnd_v20_boosted_body'].node_tree.nodes["Image Texture.003"]), ('Group', bpy.data.materials['bloodhound_lgnd_v20_boosted_body'].node_tree.nodes["Group"])

>>> nodes['Image Texture'].image.filepath
'C:\\JUDY-NB_D\\Apex Archive\\Bloodhound model\\pilot_medium_bloodhound_season_06_heist\\_images\\bloodhound_lgnd_v20_boosted_body_albedoTexture.png'

>>> bpy.context.active_object
bpy.data.objects['pilot_medium_bloodhound_season_06_heist_LOD0_skel']

>>> bpy.context.active_object.children
(bpy.data.objects['pilot_medium_bloodhound_season_06_heist_LOD0_SEModelMesh.029'], bpy.data.objects['pilot_medium_bloodhound_season_06_heist_LOD0_SEModelMesh.030'], bpy.data.objects['pilot_medium_bloodhound_season_06_heist_LOD0_SEModelMesh.031'])

>>> bpy.context.active_object.children[0]
bpy.data.objects['pilot_medium_bloodhound_season_06_heist_LOD0_SEModelMesh.029']

>>> bpy.context.active_object.children[0].type
'MESH'

>>> bpy.context.active_object.type
'ARMATURE

>>> gear.node_tree.nodes.remove(gear.node_tree.nodes['Principled BSDF'])

# https://docs.blender.org/api/blender_python_api_2_77_1/bpy.types.BlendDataLibraries.html
filepath = "C:\\JUDY-NB_D\\Apex Archive\\Apex Shader.blend"
with bpy.data.libraries.load(filepath) as (data_from, data_to):
    data_to.node_tree = data_from.node_tree

>>> data_from.node_groups
['Cores Apex Shader  1.3']

# https://blender.stackexchange.com/questions/150874/python-add-existing-nodegroup-to-material
def instantiate_group(nodes, data_block_name):
    group = nodes.new(type='ShaderNodeGroup')
    group.node_tree = bpy.data.node_groups[data_block_name]
    return group
test_group.links.new(test_group.inputs[0], node_add.inputs[0])
test_group.links.new(node_add.outputs[0], test_group.outputs[0])

>>> mat.node_tree.nodes['Group'].inputs.keys(
['Cycles//Eevee', 'Albedo', 'Specular', 'Glossy', 'Normal', ' ', 'AO', 'AO Strength', 'Cavity', 'Cavity Strength', ' ', 'Emission', 'Emission Color', 'Emission Strength', ' ', 'Subsurface', 'Subsurface Color', ' ', 'Cycles Specular', 'Cycles  Metalic', 'Cycles Color Spec Metalic'

"C:\\JUDY-NB_D\\Apex Archive\\Bloodhound model\\bloodhound_v20_ascension_w\\_images\\bloodhound_lgnd_v20_ascension_body_albedoTexture.png"
"""

import bpy
from . import config
import glob
from pathlib import Path
from bpy import context
from collections import defaultdict
from node_adder import *



def shadeMesh(mesh: bpy.types.Object, node_adder_cls: NodeAdder):
    print(f"[*] shadeMesh({mesh})")
    mat = mesh.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # take any Image Texture available
    img_texture = [node for node in nodes.values() if node.type == 'TEX_IMAGE'][0]
    # (blender use leading double slash `//` as relpath. use bpy first to make it absolute for pathlib)
    img_path = Path(bpy.path.abspath(img_texture.image.filepath))

    # clear field
    nodes.clear()
    
    # make some nodes
    cas_node_group = nodes.new(type='ShaderNodeGroup')
    cas_node_group.node_tree = node_adder_cls.getShaderNodeGroup()
    cas_node_group.location = (400.0, 0.0)
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (700.0, 0.0)
    links.new(cas_node_group.outputs[0], output_node.inputs[0])

    # get path from image texture (should be .../<model_name>_<mesh_name>_<texture_name>.png)
    # (currently assume path.count("_") is the same for all texture in directory)
    mesh_name = img_path.name[:img_path.name.rindex('_')]
    texture_paths = img_path.parent.glob(mesh_name + '_*')

    # add all textures
    for i, texture_path in enumerate(texture_paths):
        ret = node_adder_cls.addImageTexture(texture_path, mat, cas_node_group, (0.0, -70.0 * i))
        print(f'     Adding texture {str(texture_path)}... {"O" if ret else "X"}')
    
    return

def shadeArmature(armature: bpy.types.Object, node_adder_cls=NodeAdder):
    print(f'[*] shadeArmature({armature})')
    meshes = [obj for obj in armature.children if obj.type == 'MESH']
    success_ls = []
    failed_ls = []

    # for i, mesh in enumerate(meshes):
    #     try:
    #         print(f'[Armature-Mesh {i}/{len(meshes)}] shading mesh {mesh}...')
    #         shadeMesh(mesh, do_check, node_adder_cls)
    #         success_ls.append(mesh)
    #     except Exception as e:
    #         print(e)
    #         failed_ls.append((mesh, e))

    # print(f'Success: ')
    # for i in success_ls:
    #     print("    ", i)
    # print(f'Failed: ')
    # for i in failed_ls:
    #     print("    ", i)
    
    # if len(failed_ls) != 0:
    #     raise Exception(f"Exception occured when shading those meshes: {failed_ls}")
    # return
    for i, mesh in enumerate(meshes):
        print(f'[Armature-Mesh {i}/{len(meshes)}] shading mesh {mesh}...')
        shadeMesh(mesh, node_adder_cls)

def removeTextureMesh(mesh: bpy.types.Object, texture_type: str):
    """
        remove texture (by directly removing that image texture)
        # e.g. if you want to remove `octane_base_body_scatterThicknessTexture`,
        # then texture_type = 'scatterThicknessTexture'
    """
    print(f'[*] removeTextureMesh({mesh}, {texture_type})')
    mat = mesh.active_material
    nodes = mat.node_tree.nodes

    img_textures = [node for node in nodes.values() if node.type == 'TEX_IMAGE']

    for img_texture in img_textures:
        img_path = Path(bpy.path.abspath(img_texture.image.filepath))
        if img_path.stem[img_path.stem.rindex('_')+1:] == texture_type:
            print(f'    removed {str(img_path.stem)}')
            nodes.remove(img_texture)

def removeTextureArmature(armature: bpy.types.Object, texture_type: str):
    print(f'[*] removeTextureArmature({armature}, {texture_type})')
    meshes = [obj for obj in armature.children if obj.type == 'MESH']
    success_ls = []
    failed_ls = []

    # for i, mesh in enumerate(meshes):
    #     try:
    #         print(f"[Armature-Mesh {i}/{len(meshes)}] removing texture '{texture_type}' from mesh {mesh}...")
    #         removeTextureMesh(mesh, texture_type)
    #         success_ls.append(mesh)
    #     except Exception as e:
    #         print(e)
    #         failed_ls.append((mesh, e))

    # print(f'Shade Success: ')
    # for i in success_ls:
    #     print("    ", i)
    # print(f'Shade Failed: ')
    # for i in failed_ls:
    #     print("    ", i)
    
    # if len(failed_ls) != 0:
    #     raise Exception(f"Exception occured when removing textures '{texture_type}' from those meshes: {failed_ls}")
    for i, mesh in enumerate(meshes):
        print(f"[Armature-Mesh {i}/{len(meshes)}] removing texture '{texture_type}' from mesh {mesh}...")
        removeTextureMesh(mesh, texture_type)
        success_ls.append(mesh)
    return

def recolorMesh(mesh: bpy.types.Object, dir_path: Path, node_adder_cls: NodeAdder):
    """
        make a recolor material for the mesh, using the materials from `dir_path`

        dir_path: the directory where the textures of this material is stored
    """
    print(f'[*] recolorMesh({mesh}, {dir_path.stem} ({str(dir_path)}))')

    # see if this texture is loaded already
    mat = bpy.data.materials.get(f"{dir_path.stem}_material")
    if mat is not None:
        # already have this texture, reuse it
        if mesh.data.materials:
            mesh.data.materials[0] = mat
        else:
            mesh.data.materials.append(mat)
        mesh.active_material = mat
        return
    
    # add new material for this recolor's mesh
    mat = bpy.data.materials.new(name=f"{dir_path.stem}_material")
    if mesh.data.materials:
        mesh.data.materials[0] = mat
    else:
        mesh.data.materials.append(mat)
    mesh.active_material = mat
    mat.use_nodes = True   # to make node tree, or else mat.node_tree is None
    nodes = mat.node_tree.nodes

    # pick whatever image and use it as image node
    img_path = next(dir_path.iterdir())
    nodes.clear()
    img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
    img_node.image = bpy.data.images.load(str(img_path))

    # shadeMesh will use that image node and import other things
    shadeMesh(mesh, node_adder_cls)

def recolorArmature(armature: bpy.types.Object, dir_path: Path, node_adder_cls: NodeAdder):
    print(f'[*] recolorArmature({armature}, {dir_path})')
    meshes = [obj for obj in armature.children if obj.type == 'MESH']

    # make mapping from name of mesh to mesh, name is derived from image texture path
    # note that one name may map to multiple mesh,
    # e.g. in pilot_heavy_revenant_legendary_02, mesh `hand` and `body` both uses `body` texture...
    mesh_name_map = defaultdict(list)
    for mesh in meshes:
        mat = mesh.active_material
        nodes = mat.node_tree.nodes
        img_texture = [node for node in nodes.values() if node.type == 'TEX_IMAGE'][0]
        img_path = Path(bpy.path.abspath(img_texture.image.filepath))

        # e.g. "bloodhound_lgnd_v21_chinatown_body_aoTexture.png" -> name = "body"
        name = img_path.stem.split('_')[-2]
        mesh_name_map[name].append(mesh)
    
    # find all similarly named directory and use them to recolor
    # success_ls = []
    # failed_ls = []
    # dir_name = dir_path.stem                        # e.g. "bloodhound_base_body"
    # recolor_name = dir_name[:dir_name.rindex('_')]  # e.g. "bloodhound_base"
    # for subdir_path in dir_path.parent.glob(recolor_name + '*'):
    #     if not subdir_path.is_dir():
    #         continue
    #     if subdir_path.stem.count('_') != dir_name.count('_'):
    #         # e.g. when choosing "bloodhound_lgnd_v21_heroknight_gear",
    #         # cannot import "bloodhound_lgnd_v21_heroknight_rt01_body"
    #         continue
    #     name = subdir_path.stem.split('_')[-1]  # e.g. "bloodhound_base_fur" -> "fur"
    #     if name in mesh_name_map:
    #         try:
    #             for mesh in mesh_name_map[name]:
    #                 recolorMesh(mesh, subdir_path)
    #                 success_ls.append(mesh)
    #         except Exception as e:
    #             print(e)
    #             failed_ls.append((mesh, e))
    
    # print(f'Recolor Success: ')
    # for i in success_ls:
    #     print("    ", i)
    # print(f'Recolor Failed: ')
    # for i in failed_ls:
    #     print("    ", i)
    
    # if len(failed_ls) != 0:
    #     raise Exception(f"Exception occured when recoloring those meshes: {failed_ls}")
    dir_name = dir_path.stem                        # e.g. "bloodhound_base_body"
    recolor_name = dir_name[:dir_name.rindex('_')]  # e.g. "bloodhound_base"
    for subdir_path in dir_path.parent.glob(recolor_name + '*'):
        if not subdir_path.is_dir():
            continue
        if subdir_path.stem.count('_') != dir_name.count('_'):
            # e.g. when choosing "bloodhound_lgnd_v21_heroknight_gear",
            # cannot import "bloodhound_lgnd_v21_heroknight_rt01_body"
            continue
        name = subdir_path.stem.split('_')[-1]  # e.g. "bloodhound_base_fur" -> "fur"
        if name in mesh_name_map:
            for mesh in mesh_name_map[name]:
                recolorMesh(mesh, subdir_path, node_adder_cls)
    return