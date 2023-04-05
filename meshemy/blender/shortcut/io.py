import bpy


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


def load_mesh_into_object(name: str, mesh, with_collection: bool = False) -> None:
    # make object from mesh
    new_object = bpy.data.objects.new(name, mesh)

    if with_collection:
        new_collection = bpy.data.collections.new("Collection")
        bpy.context.scene.collection.children.link(new_collection)

        # add object to scene collection
        new_collection.objects.link(new_object)

    return new_object
