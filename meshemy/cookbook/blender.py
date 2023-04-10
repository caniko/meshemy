import logging
from functools import cached_property
from typing import Optional

import bpy
import numpy as np
from bmesh.types import BMesh
from pydantic import FilePath, computed_field
from pydantic_numpy import NpNDArray
from pydantic_numpy.typing import NpNDArrayFp64

from meshemy.blender.constant import SUFFIX_TO_READER, SUFFIX_TO_WRITER
from meshemy.blender.shortcut.io import load_mesh_from_numpy_arrays
from meshemy.blender.shortcut.select import (
    get_latest_object_created,
    get_object_by_name,
    set_object_active_by_name,
)
from meshemy.blender.utils import safely_enter_mode, triangular_bmesh
from meshemy.blender.workflows import (
    add_simple_material,
    merge_close,
    planar_decimate_mesh,
)
from meshemy.cookbook.base import BaseCookbook

logger = logging.getLogger(__file__)


class BlenderCookbook(BaseCookbook):
    mesh_name: str

    cached_bm: BMesh | None = None

    def reset_bm(self) -> None:
        self.cached_bm = None

    @computed_field(return_type=BMesh)  # type: ignore[misc]
    @property
    def triangular_bmesh(self) -> BMesh:
        if not self.cached_bm:
            self.cached_bm = triangular_bmesh(mesh_object_name=self.mesh_name)
        return self.cached_bm

    @computed_field(return_type=NpNDArrayFp64 | None)  # type: ignore[misc]
    @property
    def vertices_numpy_array(self) -> NpNDArrayFp64 | None:
        return np.array([v.co.copy() for v in self.triangular_bmesh.verts], dtype=np.float64)

    @computed_field(return_type=NpNDArray | None)  # type: ignore[misc]
    @property
    def edges_numpy_array(self) -> NpNDArray | None:
        return np.array([[v.index for v in e.verts] for e in self.triangular_bmesh.edges])

    @computed_field(return_type=NpNDArray | None)  # type: ignore[misc]
    @property
    def faces_numpy_array(self) -> NpNDArray | None:
        return np.array([[v.index for v in f.verts] for f in self.triangular_bmesh.faces])

    @cached_property
    def watertight(self) -> bool:
        for edge in self.triangular_bmesh.edges:
            if len(edge.link_faces) != 2:
                return False
        return True

    def planar_decimate(self, degree_tol: float) -> "BlenderCookbook":
        planar_decimate_mesh(degree_tol, mesh_object_name=self.mesh_name)
        logger.debug(f"Planar decimation on {self.mesh_name}, degree tolerance {degree_tol}")
        self.reset_bm()
        return self

    def merge_close(self, distance_tol: float) -> "BlenderCookbook":
        merge_close(distance_tol, mesh_object_name=self.mesh_name)
        logger.debug(f"Merging proximal vertices on {self.mesh_name}, distance tolerance {distance_tol}")
        self.reset_bm()
        return self

    def add_simple_material(self, color: tuple[float, float, float, float]) -> "BlenderCookbook":
        # Define the color as an RGBA tuple (red, green, blue, alpha)
        add_simple_material(self.mesh_name, color)
        return self

    def translate(self, xyz: tuple[float, float, float]) -> "BlenderCookbook":
        obj = self._get_object()
        obj.location = tuple(xyz)
        return self

    def rotate(self, xyz: tuple[float, float, float]) -> "BlenderCookbook":
        obj = self._get_object()
        obj.rotation_euler = tuple(xyz)
        return self

    def scale(self, xyz: tuple[float, float, float]) -> "BlenderCookbook":
        obj = self._get_object()
        obj.scale = tuple(xyz)
        return self

    def move2origin(self) -> "BlenderCookbook":
        safely_enter_mode("OBJECT")

        _obj = self._set_to_active()

        # Set the object's origin to its geometry center based on its bounding box
        bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")

        return self

    def select(self) -> "BlenderCookbook":
        set_object_active_by_name(self.mesh_name)
        return self

    def save(self, path: FilePath) -> None:
        _ob = self._set_to_active()
        SUFFIX_TO_WRITER[path.suffix](filepath=str(path))

    @classmethod
    def from_data(cls, name: str = "new_object", **kwargs) -> "BlenderCookbook":
        load_mesh_from_numpy_arrays(name=name, **kwargs)
        return cls(mesh_name=name)

    @classmethod
    def from_file(cls, path: FilePath, name: Optional[str] = None, **kwargs) -> "BlenderCookbook":
        SUFFIX_TO_READER[path.suffix](filepath=str(path), **kwargs)
        if name:
            obj = get_latest_object_created()
            obj.name = name
            obj.data.name = f"mesh_{name}"
        else:
            name = get_latest_object_created().name

        return cls(mesh_name=name)

    def _get_object(self):
        return get_object_by_name(self.mesh_name)

    def _set_to_active(self):
        return set_object_active_by_name(self.mesh_name)
