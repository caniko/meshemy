import logging
from typing import Optional

import bpy
import numpy as np
from bmesh.types import BMesh
from pydantic import FilePath
from pydantic_numpy import NDArray, NDArrayFp64

from meshemy.blender.constant import SUFFIX_TO_READER, SUFFIX_TO_WRITER
from meshemy.blender.shortcut.select import latest_mesh, select_object
from meshemy.blender.utils import load_mesh_from_numpy_arrays, triangular_bmesh
from meshemy.blender.workflows import merge_close, planar_decimate_mesh
from meshemy.cookbook.base import BaseCookbook

logger = logging.getLogger(__file__)


class BlenderCookbook(BaseCookbook):
    mesh_name: str

    cached_bm: BMesh | None

    def reset_bm(self) -> None:
        self.cached_bm = None

    @property
    def triangular_bmesh(self) -> BMesh:
        if not self.cached_bm:
            self.cached_bm = triangular_bmesh(mesh_object_name=self.mesh_name)
        return self.cached_bm

    @property
    def vertices_numpy_array(self) -> NDArrayFp64 | None:
        return np.array([v.co.copy() for v in self.triangular_bmesh.verts], dtype=np.float64)

    @property
    def edges_numpy_array(self) -> NDArray | None:
        return np.array([[v.index for v in e.verts] for e in self.triangular_bmesh.edges])

    @property
    def faces_numpy_array(self) -> NDArray | None:
        return np.array([[v.index for v in f.verts] for f in self.triangular_bmesh.faces])

    @property
    def watertight(self) -> bool:
        for edge in self.triangular_bmesh.edges:
            if len(edge.link_faces) != 2:
                return False
        return True

    def planar_decimate(self, degree_tol: float) -> None:
        planar_decimate_mesh(degree_tol, mesh_object_name=self.mesh_name)
        logger.debug(f"Planar decimation on {self.mesh_name}, degree tolerance {degree_tol}")
        self.reset_bm()

    def merge_close(self, distance_tol: float) -> None:
        merge_close(distance_tol, mesh_object_name=self.mesh_name)
        logger.debug(f"Merging proximal vertices on {self.mesh_name}, distance tolerance {distance_tol}")
        self.reset_bm()

    def save(self, path: FilePath) -> None:
        _ob = select_object(self.mesh_name)
        SUFFIX_TO_WRITER[path.suffix](filepath=str(path))

    @classmethod
    def from_data(
        cls, vertices: NDArrayFp64, edges: NDArray | None, faces: NDArray | None, name: str = "new_object"
    ) -> "BlenderCookbook":
        load_mesh_from_numpy_arrays(vertices, edges, faces, name)
        return cls(mesh_name=name)

    @classmethod
    def from_file(cls, path: FilePath, name: Optional[str] = None, **kwargs) -> "BlenderCookbook":
        SUFFIX_TO_READER[path.suffix](filepath=str(path), **kwargs)
        if name:
            ob = latest_mesh()
            ob.name = name
            ob.data.name = name
        else:
            name = latest_mesh().name

        return cls(mesh_name=name)
