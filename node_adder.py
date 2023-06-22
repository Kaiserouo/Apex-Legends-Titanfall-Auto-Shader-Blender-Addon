import bpy
from . import config
from pathlib import Path

class NodeAdder:
    """
        The class used for adding image shader nodes

        Note that since the image texture might be removed by "Remove Texture",
        you must guarentee that even if the image texture is directly removed,
        the rest of nodes you add won't affect the outcome.
    """
    @staticmethod
    def getShaderNodeGroup():
        """
            Return a node group. This will become a node and will be passed
            into addImageTexture() later.

            This will be called once every time a material is shaded.

            You can also return an empty node group and don't use this in addImageTexture...
        """
        raise NotImplementedError()

    @classmethod
    def addImageTexture(cls, img_path: Path, mat, shader_node_group, location=(0.0, 0.0)):
        """
            Given an image specified by `img_path`, attach that image to its appropriate position.
            Need to handle the creation of image node.

            shader_node_group is a node that is created by the node tree from getShaderNodeGroup()
            location should be the position of the image node (but not necessarily).
        """
        raise NotImplementedError()
        
class CoresNodeAdder(NodeAdder):
    """
        Cores Apex Shader from `Apex Shader.blend`
        credits `CoReArtZz` 
        ref. https://www.reddit.com/r/apexlegends/comments/jtg4a7/basic_guide_to_render_apex_legends_models_in/
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

    @staticmethod
    def getShaderNodeGroup():
        filepath = config.CORE_APEX_SHADER_BLENDER_FILE

        # use cached node group for the same file if already loaded from file before
        # (cached in CoresNodeAdder since this should stay the same)
        cached_group = getattr(CoresNodeAdder, 'cached_group', None)
        if cached_group is not None:
            print(f'used cache node group: {filepath}')
            return cached_group
        
        
        print(f'import node group from file: {filepath}')
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.node_groups = data_from.node_groups
        # just return any core apex shader in there
        for group in data_to.node_groups:
            if 'Cores Apex Shader' in group.name:
                CoresNodeAdder.cached_group = group
                return group
        else:
            raise Exception(f'No "Cores Apex Shader" node tree in {filepath}.')

    @classmethod
    def addImageTexture(cls, img_path, mat, cas_node_group, location=(0.0, 0.0)):
        # get name
        texture_name = img_path.stem[img_path.stem.rindex('_')+1:]
        if texture_name not in cls.method.keys():
            return False
        # add texture
        cls.method[texture_name](img_path, mat, cas_node_group, location)
        return True
        
class PlusNodeAdder(NodeAdder):
    """
        Apex Shader Plus from `Apex_Shader_Plus1.blend`
        credits `unknown` 
        ref. https://github.com/ovlack/apex-info/commit/a9ec3ff2fab88546b8f91c1d62fd399652fe23c2/
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
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Normal Map'])

    @staticmethod
    def _addAO(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['AO (Ambient Occlussion)'])

    @staticmethod
    def _addGlossy(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Glossiness'])

    @staticmethod
    def _addEmmisive(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Emission'])
    
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
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['SSS (Subsurface Scattering)'])
        mat.node_tree.links.new(img_node.outputs['Alpha'], cas_node_group.inputs['SSS Alpha'])
        cas_node_group.inputs['SSS Strength'].default_value = 0.5
    
    @staticmethod
    def _addAnisoSpecDir(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Anis-SpecDir'])
    
    @staticmethod
    def _addTransmittanceTint(img_path, mat, cas_node_group, location):
        pass
    
    @staticmethod
    def _addOpacityMultiply(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Alpha//OpacityMult'])
        
    
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

    @staticmethod
    def getShaderNodeGroup():
        filepath = config.PLUS_APEX_SHADER_BLENDER_FILE

        # use cached node group for the same file if already loaded from file before
        # (cached in CoresNodeAdder since this should stay the same)
        cached_group = getattr(PlusNodeAdder, 'cached_group', None)
        if cached_group is not None:
            print(f'used cache node group: {filepath}')
            return cached_group
        
        
        print(f'import node group from file: {filepath}')
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.node_groups = data_from.node_groups
        # just return any core apex shader in there
        for group in data_to.node_groups:
            if 'Apex Shader+' in group.name:
                PlusNodeAdder.cached_group = group
                return group
        else:
            raise Exception(f'No "Apex Shader+" node tree in {filepath}.',)

    @classmethod
    def addImageTexture(cls, img_path, mat, cas_node_group, location=(0.0, 0.0)):
        # get name
        texture_name = img_path.stem[img_path.stem.rindex('_')+1:]
        if texture_name not in cls.method.keys():
            return False
        # add texture
        cls.method[texture_name](img_path, mat, cas_node_group, location)
        return True

class PathfinderEmoteNodeAdder(CoresNodeAdder):
    """
        Translate UV map for emote's albedo texture to use different emote.
        TextureCoordinate.UV + (x, y, 0) to access all 12 emotes, where
        - x in [0, 0.25, 0.5, 0.75]
        - y in [0, 0.375, 0.63]

        The actual node group's specification are:

        value = getValueInput()             # increment 0.1
        v1 = truncate((value + 24) * 10)    # +24 because if value start at 0 then some emotes will
                                            # repeat frequently, for unknown reason
        x = (v1 % 4) * 0.25
        v2 = truncate(v1 / 4) % 3
        y = (v2 > 0.1) * 0.375 + (v2 > 1.1) * 0.255
        output = getTexCoordUVInput() + (x, y, 0)

        connect output to albedo texture's vector input.
    """
    @staticmethod
    def getPathfinderUVTransformNodeGroup():
        # the node group spec above is from a built-in node.

        filepath = config.BUILTIN_BLENDER_FILE

        # use cached node group for the same file if already loaded from file before
        cached_group = getattr(PathfinderEmoteNodeAdder, 'cached_pf_group', None)
        if cached_group is not None:
            print(f'used cache node group: {filepath}')
            return cached_group
        
        
        print(f'import node group from file: {filepath}')
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.node_groups = data_from.node_groups
        for group in data_to.node_groups:
            if 'Pathfinder Emote UV Transform Node' in group.name:
                PathfinderEmoteNodeAdder.cached_pf_group = group
                return group
        else:
            raise Exception(f'No "Pathfinder Emote UV Transform Node" node tree in {filepath}.')
        
    @staticmethod
    def _addAlbedo(img_path, mat, cas_node_group, location):
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.hide = True
        img_node.location = location
        img_node.image = bpy.data.images.load(str(img_path))
        mat.node_tree.links.new(img_node.outputs['Color'], cas_node_group.inputs['Albedo'])

        path_node_group = mat.node_tree.nodes.new(type='ShaderNodeGroup')
        path_node_group.node_tree = PathfinderEmoteNodeAdder.getPathfinderUVTransformNodeGroup()
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


    method = CoresNodeAdder.method.copy()
    method['albedoTexture'] = _addAlbedo