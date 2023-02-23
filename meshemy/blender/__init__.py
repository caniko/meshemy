from meshemy.utility.exception import blender_module_not_installed_error

try:
    import bpy
except ModuleNotFoundError as e:
    blender_module_not_installed_error(e)
