from pathlib import Path

import numpy as np
import trimesh
from pydantic_numpy import NDArray, NDArrayFp64

from meshemy.cookbook.base import MeshIsObjectMixin, BaseCookbook


class TrimeshCookbook(BaseCookbook, MeshIsObjectMixin[trimesh.Trimesh]):
    @property
    def vertices_numpy_array(self) -> NDArrayFp64 | None:
        return self.mesh.vertices

    @property
    def edges_numpy_array(self) -> NDArray | None:
        return np.array(self.mesh.edges)

    @property
    def faces_numpy_array(self) -> NDArray | None:
        return self.mesh.faces

    def save(self, save_path: Path | str) -> None:
        self.mesh.export(save_path)
