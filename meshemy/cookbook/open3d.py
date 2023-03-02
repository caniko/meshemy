from functools import partial

from pydantic.generics import GenericModel

try:
    import open3d as o3d
except ModuleNotFoundError as e:
    from meshemy.utility.exception import open3d_module_not_installed_error

    open3d_module_not_installed_error(e)

import logging
from pathlib import Path

import numpy as np
from pydantic_numpy import NDArray, NDArrayFp64

from meshemy.cookbook.base import BaseCookbook, MeshIsObjectMixin
from meshemy.utility.io import o3d_from_vertices_faces
from meshemy.utility.seal import seal_mesh

logger = logging.getLogger(__file__)


class Open3dCookbook(BaseCookbook, MeshIsObjectMixin[o3d.geometry.TriangleMesh]):
    mesh_from_file_loader = o3d.io.read_triangle_mesh

    @property
    def vertices_numpy_array(self) -> NDArrayFp64 | None:
        return np.asarray(self.mesh.vertices)

    @property
    def edges_numpy_array(self) -> NDArray | None:
        return logger.debug("Open3D does not expose the edges of its mesh")

    @property
    def faces_numpy_array(self) -> NDArray | None:
        return np.asarray(self.triangles)

    def smoothen(self, iterations: int, copy: bool = False) -> None:
        result = self.mesh.filter_smooth_taubin(number_of_iterations=iterations)
        if copy:
            self.__class__(mesh=result)
        self.mesh = result

    def attempt_seal_insurance(self) -> bool:
        # TODO: Fix crash
        # Perform seal only if mesh is leaky, ie not watertight
        if not self.watertight:
            logger.debug(f"Attempting to seal mesh")
            self.mesh = o3d_from_vertices_faces(*seal_mesh(self.vertices.copy(), self.faces.copy()))
            if self.mesh.is_watertight():
                logger.debug(f"The seal was success!")
            else:
                logger.debug(f"Failed to seal!")
                return False
        return True

    def repair(self) -> None:
        self.mesh = (
            self.mesh.remove_duplicated_triangles()
            .remove_duplicated_vertices()
            .remove_degenerate_triangles()
            .remove_unreferenced_vertices()
        )

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

    def save(self, save_path: Path | str) -> None:
        o3d.io.write_triangle_mesh(
            str(save_path),
            self.mesh,
            write_vertex_colors=False,
            write_triangle_uvs=False,
        )

    @classmethod
    def from_data(cls, vertices: NDArrayFp64, faces: NDArray) -> "Open3dCookbook":
        return cls(mesh=o3d_from_vertices_faces(vertices, faces))
