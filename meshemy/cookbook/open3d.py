from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import open3d as o3d
from pydantic import BaseModel
from pydantic_numpy import NDArray

from meshemy.blender.utils import load_mesh_from_o3d
from meshemy.utility.io import o3d_from_vertices_faces
from meshemy.utility.seal import seal_mesh

if TYPE_CHECKING:
    from meshemy.cookbook.blender import BlenderCookbook


class Open3dCookbook(BaseModel):
    mesh: o3d.geometry.TriangleMesh

    class Config:
        arbitrary_types_allowed = True

    def smoothen(self, iterations: int, copy: bool = False) -> None:
        result = self.mesh.filter_smooth_taubin(number_of_iterations=iterations)
        if copy:
            self.__class__(mesh=result)
        self.mesh = result

    @property
    def vertices(self) -> NDArray:
        return np.asarray(self.mesh.vertices)

    @property
    def faces(self) -> NDArray:
        return np.asarray(self.mesh.triangles)

    @property
    def triangles(self) -> NDArray:
        return self.faces

    @property
    def watertight(self) -> bool:
        return self.mesh.is_watertight()

    def attempt_seal_insurance(self) -> None:
        # Perform seal only if mesh is leaky, ie not watertight
        if not self.watertight:
            self.mesh = o3d_from_vertices_faces(*seal_mesh(self.vertices, self.faces))

    def repair(self) -> None:
        self.mesh = (
            self.mesh.remove_duplicated_triangles()
            .remove_duplicated_vertices()
            .remove_degenerate_triangles()
            .remove_unreferenced_vertices()
        )

    def to_blender(self, name: str) -> "BlenderCookbook":
        from meshemy.cookbook.blender import BlenderCookbook

        _ob = load_mesh_from_o3d(self.mesh, name)
        return BlenderCookbook(mesh_name=name)

    def save(self, path: Path, mesh_format: str = ".glb") -> None:
        open3d_triangular_mesh = (
            self.mesh.remove_duplicated_triangles()
            .remove_duplicated_vertices()
            .remove_degenerate_triangles()
            .remove_unreferenced_vertices()
        )
        o3d.io.write_triangle_mesh(
            str(path.with_suffix(mesh_format)),
            open3d_triangular_mesh,
            write_vertex_colors=False,
            write_triangle_uvs=False,
        )
