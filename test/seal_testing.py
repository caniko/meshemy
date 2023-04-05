import numpy as np
import open3d as o3d
import pymeshfix

from meshemy.cookbook.open3d import Open3dCookbook

mesh = o3d.io.read_triangle_mesh("/test/monkey.glb")
vertices = np.asarray(mesh.vertices)
faces = np.asarray(mesh.triangles)

pymeshfix.clean_from_arrays(vertices, faces, verbose=False)


mesh = Open3dCookbook.from_file("/test/monkey.glb")
mesh.attempt_seal_insurance()
