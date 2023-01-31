from typing import Optional

import bpy
import numpy as np

from meshemy.blender.shortcut import select_object, select_one_or_all


def planar_decimate_mesh(degrees: float = 1.0, mesh_object_name: Optional[str] = None) -> None:
    ob = select_object(mesh_object_name)

    bpy.ops.object.mode_set(mode="OBJECT")

    bpy.ops.object.modifier_add(type="DECIMATE")
    ob.modifiers["Decimate"].decimate_type = "DISSOLVE"
    ob.modifiers["Decimate"].angle_limit = np.deg2rad(degrees)

    bpy.ops.object.modifier_apply(modifier="Decimate")


def merge_close(tolerance: float = 0.01, mesh_object_name: Optional[str] = None) -> None:
    _ob = select_one_or_all(mesh_object_name)

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.remove_doubles(threshold=tolerance)
