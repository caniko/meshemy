import logging
from typing import Optional

import bpy
from ordered_set import OrderedSet

from meshemy.blender.utils import safely_enter_mode

logger = logging.getLogger(__file__)


def get_object_by_name(name: str):
    return bpy.data.objects.get(name)


def set_object_active_by_name(name: str):
    safely_enter_mode("OBJECT")
    obj = get_object_by_name(name)
    if obj is None:
        raise ValueError(f"Object with name {name} does not exist")

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    return obj


def select_one_or_all(name: Optional[str] = None) -> None:
    if name:
        return set_object_active_by_name(name)
    bpy.ops.mesh.select_all(action="SELECT")


def all_meshes_in_scene() -> OrderedSet:
    return OrderedSet([o for o in bpy.context.scene.objects if o.type == "MESH"])


def get_last_selection():
    return bpy.context.selected_objects[0]


get_latest_object_created = get_last_selection
