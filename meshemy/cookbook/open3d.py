from functools import cached_property

from pydantic import computed_field
from pydantic_numpy.typing import NpNDArrayFp64

try:
    import open3d as o3d
except ModuleNotFoundError as e:
    from meshemy.utility.exception import open3d_module_not_installed_error

    open3d_module_not_installed_error(e)

import logging
from pathlib import Path

import numpy as np
from pydantic_numpy import NpNDArray

from meshemy.cookbook.base import BaseCookbook, MeshIsObjectMixin
from meshemy.utility.io import o3d_from_vertices_faces

logger = logging.getLogger(__file__)


class Open3dCookbook(BaseCookbook, MeshIsObjectMixin[o3d.geometry.TriangleMesh]):
    mesh_from_file_loader = o3d.io.read_triangle_mesh

    @computed_field(return_type=NpNDArrayFp64 | None)  # type: ignore[misc]
    @property
    def vertices_numpy_array(self) -> NpNDArrayFp64 | None:
        return np.asarray(self.mesh.vertices)

    @computed_field(return_type=NpNDArray | None)  # type: ignore[misc]
    @property
    def edges_numpy_array(self) -> None:
        return None

    @computed_field(return_type=NpNDArray | None)  # type: ignore[misc]
    @property
    def faces_numpy_array(self) -> NpNDArray | None:
        return np.asarray(self.triangles)

    def smoothen(self, iterations: int, copy: bool = False) -> None:
        result = self.mesh.filter_smooth_taubin(number_of_iterations=iterations)
        if copy:
            self.__class__(mesh=result)
        self.mesh = result

    def repair(self) -> None:
        self.mesh = (
            self.mesh.remove_duplicated_triangles()
            .remove_duplicated_vertices()
            .remove_degenerate_triangles()
            .remove_unreferenced_vertices()
        )

    @computed_field(return_type=NpNDArray)  # type: ignore[misc]
    @property
    def vertices(self) -> NpNDArray:
        return np.asarray(self.mesh.vertices)

    @computed_field(return_type=NpNDArray)  # type: ignore[misc]
    @property
    def faces(self) -> NpNDArray:
        return np.asarray(self.mesh.triangles)

    @computed_field(return_type=NpNDArray)  # type: ignore[misc]
    @property
    def triangles(self) -> NpNDArray:
        return self.faces

    @cached_property
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
    def from_data(cls, vertices: NpNDArrayFp64, faces: NpNDArray) -> "Open3dCookbook":
        return cls(mesh=o3d_from_vertices_faces(vertices, faces))
