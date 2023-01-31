from typing import Any, Optional

import bpy


def empty_scene():
    bpy.ops.scene.new(type="EMPTY")


def load_mesh_into_object(name: str, mesh):
    # make object from mesh
    new_object = bpy.data.objects.new(name, mesh)

    # make collection
    new_collection = bpy.data.collections.new("new_collection")
    bpy.context.scene.collection.children.link(new_collection)

    # add object to scene collection
    new_collection.objects.link(new_object)

    return new_object


def select_object(name: str):
    ob = bpy.context.scene.objects[name]
    bpy.ops.object.select_all(action="DESELECT")  # Deselect all objects
    bpy.context.view_layer.objects.active = ob  # Make the cube the active object
    ob.select_set(True)
    return ob


def select_one_or_all(name: Optional[str] = None) -> Any:
    if name:
        return select_object(name)
    bpy.ops.mesh.select_all(action="SELECT")
