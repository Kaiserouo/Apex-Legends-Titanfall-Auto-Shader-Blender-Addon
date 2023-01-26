
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
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.node_groups = data_from.node_groups
    # just return any core apex shader in there
    for group in data_to.node_groups:
        if 'Cores Apex Shader' in group.name:
            return group
    else:
        raise Exception(f'No "Cores Apex Shader" node tree in {filepath}.')

class NodeAdder:
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
    def _addScatterThickness(img_path, mat, cas_node_group, location):
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

        # those are things I don't even know how to deal with
        # (or so hard to deal with I just quitted)
        'anisoSpecDirTexture': _addAnisoSpecDir,
        'scatterThicknessTexture': _addScatterThickness,
        'transmittanceTintTexture': _addTransmittanceTint,
        'opacityMultiplyTexture': _addOpacityMultiply
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

def shadeMesh(mesh: bpy.types.Object, do_check=False):
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
    img_path = Path(img_texture.image.filepath)

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
    mesh_name = img_path.name[:img_path.name.rindex('_')]
    texture_paths = img_path.parent.glob(mesh_name + '*')

    # add all textures
    for i, texture_path in enumerate(texture_paths):
        ret = NodeAdder.addImageTexture(texture_path, mat, cas_node_group, (0.0, -70.0 * i))
        print(f'[>]     Adding texture {str(texture_path)}... {"O" if ret else "X"}')
    
    return

def shadeArmature(armature: bpy.types.Object, do_check=False):
    print(f'[*] shadeArmature({armature})')
    meshes = [obj for obj in armature.children if obj.type == 'MESH']
    success_ls = []
    failed_ls = []

    for mesh in meshes:
        try:
            shadeMesh(mesh, do_check)
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

