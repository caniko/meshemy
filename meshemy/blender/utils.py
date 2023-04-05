import bmesh
import bpy
from pydantic_numpy import NDArray, NDArrayFp64

from meshemy.blender.shortcut.io import load_mesh_into_object


def load_mesh_from_numpy_arrays(
    vertices: NDArrayFp64, edges: NDArray | None, faces: NDArray | None, name: str = "new_object"
):
    assert edges is not None or faces is not None

    # https://b3d.interplanety.org/en/how-to-create-mesh-through-the-blender-python-api/
    mesh_data = bpy.data.meshes.new(name)
    mesh_data.from_pydata(
        vertices.tolist(), () if edges is None else edges.tolist(), () if faces is None else faces.tolist()
    )
    mesh_obj = bpy.data.objects.new(name, mesh_data)
    bpy.context.collection.objects.link(mesh_obj)


def triangular_bmesh(mesh_object_name: str) -> tuple[NDArrayFp64, NDArray, NDArray]:
    from meshemy.blender.shortcut.select import select_object

    _ob = select_object(mesh_object_name)

    safely_enter_mode("EDIT")
    bpy.ops.mesh.quads_convert_to_tris(quad_method="BEAUTY")
    bpy.ops.object.mode_set(mode="OBJECT")

    bm = bmesh.new()
    bm.from_mesh(select_object(mesh_object_name).data)

    return bm


def safely_enter_mode(mode_name: str) -> None:
    try:
        bpy.ops.object.mode_set(mode=mode_name)
    except RuntimeError:
        # Happens if we are in object mode already
        pass
