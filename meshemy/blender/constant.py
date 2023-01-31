import bpy

SUFFIX_TO_READER = {
    ".gltf": bpy.ops.import_scene.gltf,
    ".glb": bpy.ops.import_scene.gltf,
    # ".stl": bpy.ops.wm.stl_import,
    ".ply": bpy.ops.import_scene.ply,
    # ".obj": bpy.ops.wm.obj_import,
}
