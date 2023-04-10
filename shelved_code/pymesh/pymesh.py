from pathlib import Path
from typing import Any

import numpy as np
import pymesh
from pydantic import computed_field
from pydantic_numpy import NpNDArray
from pydantic_numpy.typing import NpNDArrayFp64

from meshemy.cookbook.base import BaseCookbook, MeshIsObjectMixin
from shelved_code.pymesh.fix_mesh import pymesh_fix_mesh


class PyMeshCookbook(BaseCookbook, MeshIsObjectMixin[Any]):
    mesh_from_file_loader = pymesh.meshio.load_mesh

    def save(self, save_path: Path | str) -> None:
        pymesh.save_mesh(str(save_path), self.mesh)

    @classmethod
    def from_data(cls, vertices: NpNDArrayFp64, faces: NpNDArray):
        return pymesh.form_mesh(vertices=vertices, faces=faces)

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

    @computed_field(return_type=bool)
    @property
    def watertight(self) -> bool:
        raise NotImplementedError()

    def fix(self, detail: str = "normal") -> None:
        self.mesh = pymesh_fix_mesh(self.mesh, detail)
