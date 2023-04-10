import bpy
from pydantic_numpy import NpNDArray
from pydantic_numpy.typing import NpNDArrayFp64

from meshemy.blender.utils import link_mesh_into_object


def delete_everything() -> None:
    # Select all objects
    bpy.ops.object.select_all(action="SELECT")

    # Delete selected objects
    bpy.ops.object.delete()

    for collection in bpy.data.collections:
        # Loop through all objects in the collection
        for obj in collection.objects:
            # Select the object
            obj.select_set(True)
        for scene in bpy.data.scenes:
            if collection.name in scene.collection.children:
                scene.collection.children.unlink(collection)

        # Delete the collection
        bpy.data.collections.remove(collection)

    # Delete selected objects
    bpy.ops.object.delete()

    # Iterate through the materials and remove them
    for material in iter(bpy.data.materials):
        bpy.data.materials.remove(material)


def load_mesh_from_numpy_arrays(
    vertices: NpNDArrayFp64, edges: NpNDArray | None, faces: NpNDArray | None, name: str = "new_object"
):
    assert edges is not None or faces is not None

    # https://b3d.interplanety.org/en/how-to-create-mesh-through-the-blender-python-api/
    mesh_data = bpy.data.meshes.new(name)
    mesh_data.from_pydata(
        vertices.tolist(), () if edges is None else edges.tolist(), () if faces is None else faces.tolist()
    )
    link_mesh_into_object(name, mesh_data)
    return mesh_data
