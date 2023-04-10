from pathlib import Path

import bpy

from meshemy.blender.workflows import add_simple_material
from meshemy.cookbook.blender import BlenderCookbook

name = "test"

mesh_obj = BlenderCookbook.from_file(Path("imma_cube.glb"), name)
add_simple_material(name, (1.0, 1.0, 0, 1.0))

mesh_obj = BlenderCookbook.from_file(Path("imma_cube.glb"), "test2")
add_simple_material("test2", (1.0, 1.0, 0, 1.0))

bpy.ops.wm.save_mainfile(filepath=str(Path(__file__).parent.absolute() / "cannon_ball.blend"))
