import bpy


def empty_scene() -> None:
    bpy.ops.scene.new(type="EMPTY")


def load_mesh_into_object(name: str, mesh) -> None:
    # make object from mesh
    new_object = bpy.data.objects.new(name, mesh)

    # make collection
    new_collection = bpy.data.collections.new("new_collection")
    bpy.context.scene.collection.children.link(new_collection)

    # add object to scene collection
    new_collection.objects.link(new_object)

    return new_object
