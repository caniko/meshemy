import bmesh
import bpy
from pydantic_numpy import NpNDArray
from pydantic_numpy.typing import NpNDArrayFp64


def triangular_bmesh(mesh_object_name: str) -> tuple[NpNDArrayFp64, NpNDArray, NpNDArray]:
    from meshemy.blender.shortcut.select import get_object_by_name

    obj = get_object_by_name(mesh_object_name)

    safely_enter_mode("EDIT")
    bpy.ops.mesh.quads_convert_to_tris(quad_method="BEAUTY")
    bpy.ops.object.mode_set(mode="OBJECT")

    bm = bmesh.new()
    bm.from_mesh(obj.data)

    return bm


def safely_enter_mode(mode_name: str) -> None:
    try:
        bpy.ops.object.mode_set(mode=mode_name)
    except RuntimeError:
        # Happens if we are in object mode already
        pass


def link_mesh_into_object(name: str, mesh_obj) -> None:
    """
    :param name: name of object with link
    :param mesh_obj: bpy.Mesh
    :return: The new object with the mesh link
    """
    return bpy.data.objects.new(name, mesh_obj)


def create_collection(name: str):
    return bpy.data.collections.new(name)


def add_object_to_collection(name: str, obj) -> None:
    new_collection = create_collection(name)
    bpy.context.scene.collection.children.link(new_collection)

    # add object to scene collection
    new_collection.objects.link(obj)
