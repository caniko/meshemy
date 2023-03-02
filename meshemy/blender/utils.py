import bmesh
import bpy
import numpy as np
import open3d as o3d
from pydantic_numpy import NDArray, NDArrayFp64

from meshemy.blender.shortcut.io import load_mesh_into_object
from meshemy.blender.shortcut.select import select_object
from meshemy.utility.io import o3d_from_vertices_faces


def load_mesh_from_numpy_arrays(
    vertices: NDArrayFp64, edges: NDArray | None, faces: NDArray | None, name: str = "new_object"
):
    assert edges is not None or faces is not None

    # https://b3d.interplanety.org/en/how-to-create-mesh-through-the-blender-python-api/
    blender_mesh = bpy.data.meshes.new(f"{name}mesh")
    blender_mesh.from_pydata(vertices, edges or (), faces or ())
    blender_mesh.update()

    return load_mesh_into_object(name, blender_mesh)


def triangular_bmesh(mesh_object_name: str) -> tuple[NDArrayFp64, NDArray, NDArray]:
    _ob = select_object(mesh_object_name)

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.quads_convert_to_tris(quad_method="BEAUTY")
    bpy.ops.object.mode_set(mode="OBJECT")

    bm = bmesh.new()
    bm.from_mesh(select_object(mesh_object_name).data)

    return bm
