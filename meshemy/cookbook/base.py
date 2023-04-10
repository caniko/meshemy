import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Generic, TypeVar, Union

import pymeshfix
from pydantic import BaseModel, FilePath
from pydantic_numpy import NpNDArray
from pydantic_numpy.typing import NpNDArrayFp64

if TYPE_CHECKING:
    from meshemy.cookbook.blender import BlenderCookbook
    from meshemy.cookbook.open3d import Open3dCookbook
    from meshemy.cookbook.trimesh import TrimeshCookbook

logger = logging.getLogger(__file__)


class BaseCookbook(BaseModel, ABC, arbitrary_types_allowed=True):   # type: ignore[call-arg]
    """
    The .from_data() and .from_file() class method also needs to be implemented, I did not make it an abstractmethod
    because each BaseCookbook has its own function signature.
    """

    @property
    @abstractmethod
    def vertices_numpy_array(self) -> NpNDArrayFp64 | None:
        ...

    @property
    @abstractmethod
    def edges_numpy_array(self) -> NpNDArray | None:
        ...

    @property
    @abstractmethod
    def faces_numpy_array(self) -> NpNDArray | None:
        ...

    @property
    @abstractmethod
    def watertight(self) -> bool:
        """Check if a mesh is watertight, also known as manifold"""
        ...

    @abstractmethod
    def save(self, save_path: Path | str) -> None:
        ...

    def attempt_seal(self):
        # Perform seal only if mesh is leaky, ie not watertight
        if not self.watertight:
            logger.debug("Mesh is leaky, attempting to seal mesh")
            fixed_vertices, fixed_faces = pymeshfix.clean_from_arrays(
                self.vertices_numpy_array.copy(), self.faces_numpy_array.copy(), verbose=False
            )
            new = self.__class__.from_data(vertices=fixed_vertices, faces=fixed_faces)

            if new.is_watertight():
                logger.debug("The seal was success!")
                return new
            else:
                logger.debug("Failed to seal!")
        else:
            logger.debug("Mesh is watertight, no action performed")

    def to_blender(self, name: str, **kwargs) -> "BlenderCookbook":
        from meshemy.cookbook.blender import BlenderCookbook

        if isinstance(self, BlenderCookbook):
            return self

        return BlenderCookbook.from_data(
            vertices=self.vertices_numpy_array,
            edges=self.edges_numpy_array,
            faces=self.faces_numpy_array,
            name=name,
            **kwargs,
        )

    def to_o3d(self) -> "Open3dCookbook":
        from meshemy.cookbook.open3d import Open3dCookbook

        if isinstance(self, Open3dCookbook):
            return self

        return Open3dCookbook.from_data(self.vertices_numpy_array, self.faces_numpy_array)

    def to_trimesh(self) -> "TrimeshCookbook":
        from meshemy.cookbook.trimesh import TrimeshCookbook

        if isinstance(self, TrimeshCookbook):
            return self

        return TrimeshCookbook.from_data(self.vertices_numpy_array, self.faces_numpy_array)


T = TypeVar("T")


class MeshIsObjectMixin(BaseModel, Generic[T]):
    mesh: T

    mesh_from_file_loader: ClassVar[Callable[[str], Any]]

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_native(cls, mesh: T) -> "MeshIsObjectMixin":
        return cls(mesh=mesh)

    @classmethod
    def from_file(cls, file_path: FilePath | str) -> "MeshIsObjectMixin":
        return cls.from_native(mesh=cls.mesh_from_file_loader(str(file_path)))
