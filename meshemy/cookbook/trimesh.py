from functools import cached_property
from typing import Sequence

from pydantic_numpy.typing import NpNDArrayFp64

try:
    import trimesh
except ModuleNotFoundError as e:
    from meshemy.utility.exception import (
        more_than_one_mesh_in_scene,
        trimesh_module_not_installed_error,
    )

    trimesh_module_not_installed_error(e)

from pathlib import Path

import numpy as np
from pydantic import FilePath, computed_field
from pydantic_numpy import NpNDArray

from meshemy.cookbook.base import BaseCookbook, MeshIsObjectMixin


def _load_trimesh(path_to_file: FilePath) -> trimesh.Trimesh:
    result = trimesh.load_mesh(path_to_file)
    if isinstance(result, trimesh.Scene):
        meshes = tuple(result.geometry.values())
        assert (number_of_meshes := len(meshes)) == 1, more_than_one_mesh_in_scene(number_of_meshes)
        result = meshes[0]
    return result


class TrimeshCookbook(BaseCookbook, MeshIsObjectMixin[trimesh.Trimesh]):
    mesh_from_file_loader = _load_trimesh

    @computed_field(return_type=NpNDArrayFp64 | None)  # type: ignore[misc]
    @property
    def vertices_numpy_array(self) -> NpNDArrayFp64 | None:
        return np.array(self.mesh.vertices)

    @computed_field(return_type=NpNDArray | None)  # type: ignore[misc]
    @property
    def edges_numpy_array(self) -> NpNDArray | None:
        return np.array(self.mesh.edges)

    @computed_field(return_type=NpNDArray | None)  # type: ignore[misc]
    @property
    def faces_numpy_array(self) -> NpNDArray | None:
        return np.array(self.mesh.faces)

    @cached_property
    def watertight(self) -> bool:
        return self.mesh.is_watertight

    @classmethod
    def from_data(cls, vertices: NpNDArray, faces: NpNDArray | None) -> "TrimeshCookbook":
        return cls(mesh=trimesh.Trimesh(vertices=vertices, faces=faces))

    def save(self, save_path: Path | str) -> None:
        self.mesh.export(save_path)

    def contains(self, vertices: Sequence[NpNDArray]) -> bool:
        return bool(np.all(self.mesh.contains(vertices)))
