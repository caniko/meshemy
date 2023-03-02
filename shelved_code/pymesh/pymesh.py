from pathlib import Path
from typing import Any

import numpy as np
import pymesh
from pydantic_numpy import NDArray, NDArrayFp64

from meshemy.cookbook.base import MeshIsObjectMixin, BaseCookbook
from meshemy.pymesh.fix_mesh import pymesh_fix_mesh


class PyMeshCookbook(BaseCookbook, MeshIsObjectMixin[Any]):
    mesh_from_file_loader = pymesh.meshio.load_mesh

    def save(self, save_path: Path | str) -> None:
        pymesh.save_mesh(str(save_path), self.mesh)

    @classmethod
    def from_data(cls, vertices: NDArrayFp64, faces: NDArray):
        return pymesh.form_mesh(vertices=vertices, faces=faces)

    @property
    def vertices_numpy_array(self) -> NDArrayFp64 | None:
        return np.array(self.mesh.vertices)

    @property
    def edges_numpy_array(self) -> NDArray | None:
        return np.array(self.mesh.edges)

    @property
    def faces_numpy_array(self) -> NDArray | None:
        return np.array(self.mesh.faces)

    def fix(self, detail: str = "normal") -> None:
        self.mesh = pymesh_fix_mesh(self.mesh, detail)
