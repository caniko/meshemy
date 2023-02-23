class BlenderNotInstalledError(ModuleNotFoundError):
    pass


class Open3DNotInstalledError(ModuleNotFoundError):
    pass


def blender_module_not_installed_error(e):
    raise BlenderNotInstalledError(
        """
        Blender module, bpy, must be installed.
        
        Please run `pip install meshemy[blender]`
        """
    ) from e


def open3d_module_not_installed_error(e):
    raise Open3DNotInstalledError(
        """
        Open3D module must be installed.

        Please run `pip install meshemy[open3d]`
        """
    ) from e
