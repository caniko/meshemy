from typing import Any, Optional

import bpy
from ordered_set import OrderedSet


def select_object(name: str):
    bpy.ops.object.mode_set(mode="OBJECT")
    ob = bpy.context.scene.objects[name]
    bpy.ops.object.select_all(action="DESELECT")  # Deselect all objects
    bpy.context.view_layer.objects.active = ob  # Make the cube the active object
    ob.select_set(True)
    return ob


def select_one_or_all(name: Optional[str] = None) -> Any:
    if name:
        return select_object(name)
    bpy.ops.mesh.select_all(action="SELECT")


def all_meshes_in_scene() -> OrderedSet:
    return OrderedSet([o for o in bpy.context.scene.objects if o.type == 'MESH'])


def latest_mesh():
    return all_meshes_in_scene()[0]
