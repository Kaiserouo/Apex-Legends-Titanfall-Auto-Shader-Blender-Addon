# basically global variables that can be configged

from pathlib import Path

# builtin blender fine
BUILTIN_BLENDER_FILE_BASE = str(Path(__file__).absolute().parent / 'asset' / 'Apex Shader.blend')
BUILTIN_BLENDER_FILE_PLUS = str(Path(__file__).absolute().parent / 'asset' / 'Apex_Shader_Plus1.blend')
BUILTIN_BLENDER_FILE_SG_SHADER = str(Path(__file__).absolute().parent / 'asset' / 'SG_Shader.blend')

# blender shader file path, the default path is the one built-in inside addon 
CORE_APEX_SHADER_BLENDER_FILE = BUILTIN_BLENDER_FILE_BASE
PLUS_APEX_SHADER_BLENDER_FILE = BUILTIN_BLENDER_FILE_PLUS
PATHFINDER_EMOTE_SHADER_BLENDER_FILE = BUILTIN_BLENDER_FILE_BASE
SG_TITANFALL_SHADER_BLENDER_FILE = BUILTIN_BLENDER_FILE_SG_SHADER