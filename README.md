# Apex Legends Auto Shader

Blender addon that auto-shades Apex Legends characters.

## How To Use
Video: https://youtu.be/p-CK_bYSK4Y

For mesh and armatures, this addon can find and import all other textures based on the auto-imported albedo texture.

`Right-click (on armature or mesh) > Apex Shader` to access the menu.

Make sure to `Apex Shader > Set Core Apex Shader blender file path` first, to use the pre-existing `Cores Apex Shader` from `Apex Shader.blend`.

## Notes
+ This will delete existing shader nodes. Should use this on newly imported models (materials).
+ Currently supported Legion-labeled textures are:
```md
[O] albedoTexture
[O] aoTexture
[O] cavityTexture
[O] emissiveTexture
[O] glossTexture
[O] normalTexture
[O] specTexture
[X] anisoSpecDirTexture
[X] scatterThicknessTexture
[X] transmittanceTintTexture
[X] opacityMultiplyTexture

... (there may be other textures not listed here)
```

## Installation
1. Clone this repository and zip it, or just download as zip file on Github.
2. `Edit -> Preferences -> Add-ons -> Install..` and choose the zip file.
3. Activate the addon by checking the box.
4. `Save Preference`