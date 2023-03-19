
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
import bpy
from bpy import context

def getCoreApexShaderNodeGroup():
    filepath = config.CORE_APEX_SHADER_BLENDER_FILE

    # use cached node group for the same file if already loaded from file before
    cached_group = getattr(getCoreApexShaderNodeGroup, 'cached_group', None)
    cached_filepath = getattr(getCoreApexShaderNodeGroup, 'filepath', None)
    if cached_group is not None and filepath == cached_filepath:
        print(f'used cache node group: {filepath}')
        return cached_group
    
    
    print(f'import node group from file: {filepath}')
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.node_groups = data_from.node_groups
    # just return any core apex shader in there
    for group in data_to.node_groups:
        if 'Cores Apex Shader' in group.name:
            getCoreApexShaderNodeGroup.cached_group = group
            getCoreApexShaderNodeGroup.filepath = filepath
            return group
    else:
        raise Exception(f'No "Cores Apex Shader" node tree in {filepath}.')

def getPathfinderUVTransformNodeGroup():
    filepath = config.CORE_APEX_SHADER_BLENDER_FILE

    # use cached node group for the same file if already loaded from file before
    cached_group = getattr(getPathfinderUVTransformNodeGroup, 'cached_group', None)
    cached_filepath = getattr(getPathfinderUVTransformNodeGroup, 'filepath', None)
    if cached_group is not None and filepath == cached_filepath:
        print(f'used cache node group: {filepath}')
        return cached_group
    
    
    print(f'import node group from file: {filepath}')
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.node_groups = data_from.node_groups
    # just return any core apex shader in there
    for group in data_to.node_groups:
        if 'Pathfinder Emote UV Transform Node' in group.name:
            getPathfinderUVTransformNodeGroup.cached_group = group
            getPathfinderUVTransformNodeGroup.filepath = filepath
            return group
    else:
        raise Exception(f'No "Pathfinder Emote UV Transform Node" node tree in {filepath}.')

class NodeAdder:
    """
        The class used for adding image shader nodes
        Note that since the image texture might be removed by "Remove Texture",
        you must guarentee that even if the image texture is directly removed,
        the rest of nodes you add won't affect the outcome
    """
    @staticmethod
    def _addAlbedo(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Albedo'])

    @staticmethod
    def _addNormal(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        img_node.image.colorspace_settings.name = 'Non-Color'
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Normal'])

    @staticmethod
    def _addAO(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['AO'])

    @staticmethod
    def _addGlossy(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Glossy'])

    @staticmethod
    def _addEmmisive(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Emission'])
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Emission Color'])
    
    @staticmethod
    def _addCavity(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Cavity'])

    @staticmethod
    def _addSpec(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Specular'])

    @staticmethod
    def _addSubsurface(img_path, mat, cas_node_group, location):
        # scatterThicknessTexture is possibly just subsurface, so that texture will use this function for now
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Subsurface'])
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Subsurface Color'])
    
    @staticmethod
    def _addAnisoSpecDir(img_path, mat, cas_node_group, location):
        pass
    
    @staticmethod
    def _addTransmittanceTint(img_path, mat, cas_node_group, location):
        pass
    
    @staticmethod
    def _addOpacityMultiply(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))

        transparent_node = mat.node_tree.nodes.new(type='ShaderNodeBsdfTransparent')
        transparent_node.location = (200, 200)
        
        mix_shader_node = mat.node_tree.nodes.new(type='ShaderNodeMixShader')
        mix_shader_node.inputs[0].default_value = 1     # so if there's no image node as input it is no-op
        mix_shader_node.location = (400, 200)

        # find output node
        output_node = [node for node in mat.node_tree.nodes.values() if node.type == 'OUTPUT_MATERIAL'][0]

        # ref. https://youtu.be/dMqk0jz749U?t=1108
        img_node.image.colorspace_settings.name = 'Non-Color'
        mat.node_tree.links.new(img_node.outputs['Color'], mix_shader_node.inputs[0])
        mat.node_tree.links.new(transparent_node.outputs[0], mix_shader_node.inputs[1])

        # should actually take whatever is linked to output_node.inputs['Surface'] as input
        # but may not be the best to assume that. oh well.
        mat.node_tree.links.new(cas_node_group.outputs[0], mix_shader_node.inputs[2])
        mat.node_tree.links.new(mix_shader_node.outputs[0], output_node.inputs['Surface'])
        mat.blend_method = 'CLIP'
        
    
    method = {
        'albedoTexture': _addAlbedo,
        'aoTexture': _addAO,
        'cavityTexture': _addCavity,
        'emissiveTexture': _addEmmisive,
        'glossTexture': _addGlossy,
        'normalTexture': _addNormal,
        'specTexture': _addSpec,
        'opacityMultiplyTexture': _addOpacityMultiply,
        'scatterThicknessTexture': _addSubsurface,

        # those are things I don't even know how to deal with
        # (or so hard to deal with I just quitted)
        'anisoSpecDirTexture': _addAnisoSpecDir,
        'transmittanceTintTexture': _addTransmittanceTint,
    }

    @classmethod
    def addImageTexture(cls, img_path, mat, cas_node_group, location=(0.0, 0.0)):
        # get name
        texture_name = img_path.stem[img_path.stem.rindex('_')+1:]
        if texture_name not in cls.method.keys():
            return False
        # add texture
        cls.method[texture_name](img_path, mat, cas_node_group, location)
        return True

class NodeAdderWithoutOpacity(NodeAdder):
    method = NodeAdder.method.copy()
    method.pop('opacityMultiplyTexture')

class PathfinderEmoteNodeAdder(NodeAdder):
    """
        Translate UV map for emote's albedo texture to use different emote.
        TextureCoordinate.UV + (x, y, 0) to access all 12 emotes, where
        - x in [0, 0.25, 0.5, 0.75]
        - y in [0, 0.375, 0.63]

        The actual node group's specification are:

        value = getValueInput()     # increment 0.1
        v1 = truncate((value + 24) * 10)
        x = (v1 % 4) * 0.25
        v2 = truncate(v1 / 4) % 3
        y = (v2 > 0.1) * 0.375 + (v2 > 1.1) * 0.255
        output = getTexCoordUVInput() + (x, y, 0)

        connect output to albedo texture's vector input.
    """
    @staticmethod
    def _addAlbedo(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Albedo'])

        path_node_group = mat.node_tree.nodes.new(type='ShaderNodeGroup')
        path_node_group.node_tree = getPathfinderUVTransformNodeGroup()
        path_node_group.hide = True
        path_node_group.location = (-200 + location[0], location[1])

        texture_coord_node = mat.node_tree.nodes.new(type='ShaderNodeTexCoord')
        texture_coord_node.hide = True
        texture_coord_node.location = (-400 + location[0], location[1] + 50)

        value_node = mat.node_tree.nodes.new(type='ShaderNodeValue')
        value_node.label = 'Value (Click its left & right button to rotate emote)'
        value_node.width = 300
        value_node.location = (-590 + location[0], location[1] - 50)

        mat.node_tree.links.new(texture_coord_node.outputs['UV'], path_node_group.inputs[0])
        mat.node_tree.links.new(value_node.outputs[0], path_node_group.inputs[1])

        mat.node_tree.links.new(path_node_group.outputs[0], img_node.inputs[0])
        return 



    method = NodeAdder.method.copy()
    method['albedoTexture'] = _addAlbedo

def shadeMesh(mesh: bpy.types.Object, do_check=False, node_adder_cls=NodeAdder):
    print(f"[*] shadeMesh({mesh})")
    mat = mesh.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    if do_check:
        # make sure this is the default one
        # i.e. only has Principled BSDF, Material Output, and Image Texture from _image/

        # i.e. only 3 things inside...
        if len(nodes.keys()) != 3:
            raise Exception(f'Should have 3 nodes only, but have {len(nodes.keys())}: {nodes.keys()}')
        
        # ...and its types are correct
        node_types = [node.type for node in nodes.values()]
        if set(['BSDF_PRINCIPLED', 'OUTPUT_MATERIAL', 'TEX_IMAGE']) != set(node_types):
            raise Exception(f"Should have type {set(['BSDF_PRINCIPLED', 'OUTPUT_MATERIAL', 'TEX_IMAGE'])}, but have {set(node_types)}")
    
    # whatever the case is, take any Image Texture available
    # (if did the check then must exist, otherwise might not exist...)
    img_texture = [node for node in nodes.values() if node.type == 'TEX_IMAGE'][0]
    # (blender use leading double slash `//` as relpath. use bpy first to make it absolute for pathlib)
    img_path = Path(bpy.path.abspath(img_texture.image.filepath))

    # clear field
    nodes.clear()
    
    # make some nodes
    cas_node_group = nodes.new(type='ShaderNodeGroup')
    cas_node_group.node_tree = getCoreApexShaderNodeGroup()
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

def shadeArmature(armature: bpy.types.Object, do_check=False, node_adder_cls=NodeAdder):
    print(f'[*] shadeArmature({armature})')
    meshes = [obj for obj in armature.children if obj.type == 'MESH']
    success_ls = []
    failed_ls = []

    for i, mesh in enumerate(meshes):
        try:
            print(f'[Armature-Mesh {i}/{len(meshes)}] shading mesh {mesh}...')
            shadeMesh(mesh, do_check, node_adder_cls)
            success_ls.append(mesh)
        except Exception as e:
            print(e)
            failed_ls.append((mesh, e))

    print(f'Success: ')
    for i in success_ls:
        print("    ", i)
    print(f'Failed: ')
    for i in failed_ls:
        print("    ", i)
    
    if len(failed_ls) != 0:
        raise Exception(f"Exception occured when shading those meshes: {failed_ls}")
    return

def removeTextureMesh(mesh: bpy.types.Object, texture_type: str):
    # remove texture (by directly removing that image texture)
    # e.g. if you want to remove `octane_base_body_scatterThicknessTexture`,
    # then texture_type = 'scatterThicknessTexture'
    print(f'[*] removeTextureMesh({mesh}, {texture_type})')
    mat = mesh.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
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

    for i, mesh in enumerate(meshes):
        try:
            print(f"[Armature-Mesh {i}/{len(meshes)}] removing texture '{texture_type}' from mesh {mesh}...")
            removeTextureMesh(mesh, texture_type)
            success_ls.append(mesh)
        except Exception as e:
            print(e)
            failed_ls.append((mesh, e))

    print(f'Success: ')
    for i in success_ls:
        print("    ", i)
    print(f'Failed: ')
    for i in failed_ls:
        print("    ", i)
    
    if len(failed_ls) != 0:
        raise Exception(f"Exception occured when removing textures '{texture_type}' from those meshes: {failed_ls}")
    return

def recolorMesh(mesh: bpy.types.Object, dir_path: Path):
    # dir_path: the directory where the textures of this material is stored
    print(f'[*] recolorMesh({mesh}, {dir_path.stem} ({str(dir_path)}))')

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
    shadeMesh(mesh)

def recolorArmature(armature: bpy.types.Object, dir_path: Path):
    print(f'[*] recolorArmature({armature}, {dir_path})')
    meshes = [obj for obj in armature.children if obj.type == 'MESH']

    # make mapping from name of mesh to mesh
    # name is derived from image texture path
    mesh_name_map = {}
    for mesh in meshes:
        mat = mesh.active_material
        nodes = mat.node_tree.nodes
        img_texture = [node for node in nodes.values() if node.type == 'TEX_IMAGE'][0]
        img_path = Path(bpy.path.abspath(img_texture.image.filepath))

        # e.g. "bloodhound_lgnd_v21_chinatown_body_aoTexture.png" -> name = "body"
        name = img_path.stem.split('_')[-2]
        mesh_name_map[name] = mesh
    
    # find all similarly named directory and use them to recolor
    success_ls = []
    failed_ls = []
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
            try:
                recolorMesh(mesh_name_map[name], subdir_path)
                success_ls.append(mesh)
            except Exception as e:
                print(e)
                failed_ls.append((mesh, e))
    
    print(f'Success: ')
    for i in success_ls:
        print("    ", i)
    print(f'Failed: ')
    for i in failed_ls:
        print("    ", i)
    
    if len(failed_ls) != 0:
        raise Exception(f"Exception occured when recoloring those meshes: {failed_ls}")
    return

