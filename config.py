# basically global variables that can be configged

from pathlib import Path

# builtin blender fine
BUILTIN_BLENDER_FILE = str(Path(__file__).absolute().parent / 'asset' / 'Apex Shader.blend')

# blender shader file path, the default path is the one built-in inside addon 
CORE_APEX_SHADER_BLENDER_FILE = BUILTIN_BLENDER_FILE