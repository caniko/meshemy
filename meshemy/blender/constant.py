from functools import partial
from typing import Callable

import bpy

SUFFIX_TO_READER = {
    ".gltf": bpy.ops.import_scene.gltf,
    ".glb": bpy.ops.import_scene.gltf,
    # ".stl": bpy.ops.wm.stl_import,
    ".ply": bpy.ops.import_scene.ply,
    # ".obj": bpy.ops.wm.obj_import,
}


def export_scene_wrapper(exporter: Callable):
    return partial(exporter, use_selection=True)


glb_gltf_export = export_scene_wrapper(bpy.ops.export_scene.gltf)

SUFFIX_TO_WRITER = {
    ".gltf": glb_gltf_export,
    ".glb": glb_gltf_export,
    # ".stl": bpy.ops.wm.stl_export,
    ".ply": export_scene_wrapper(bpy.ops.export_scene.ply),
    # ".obj": bpy.ops.wm.obj_export,
}
