from typing import Callable, Type


def _raise_not_installed_error_callable(
    exception_class: Type[Exception], name: str, extras_name: str
) -> Callable[[], None]:
    def raise_not_installed_error(e: Exception) -> None:
        raise exception_class(
            f"""
            {name} module, {extras_name}, must be installed.

            Please run `pip install meshemy[{extras_name}]`
            """
        ) from e

    return raise_not_installed_error


class BlenderNotInstalledError(ModuleNotFoundError):
    pass


class Open3DNotInstalledError(ModuleNotFoundError):
    pass


class TrimeshNotInstalledError(ModuleNotFoundError):
    pass


blender_module_not_installed_error = _raise_not_installed_error_callable(BlenderNotInstalledError, "Blender", "bpy")
open3d_module_not_installed_error = _raise_not_installed_error_callable(Open3DNotInstalledError, "Open3D", "open3d")
trimesh_module_not_installed_error = _raise_not_installed_error_callable(TrimeshNotInstalledError, "Trimesh", "trimesh")


def more_than_one_mesh_in_scene(number_of_meshes: int) -> str:
    return f"Meshemy only supports files with one mesh. More than one mesh in current scene, {number_of_meshes} meshes"
