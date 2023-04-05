import logging
from abc import ABC, abstractmethod
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Generic, TypeVar, Union

import pymeshfix
from pydantic import BaseModel, FilePath
from pydantic.generics import GenericModel
from pydantic_numpy import NDArray, NDArrayFp64

if TYPE_CHECKING:
    from meshemy.cookbook.blender import BlenderCookbook
    from meshemy.cookbook.open3d import Open3dCookbook
    from meshemy.cookbook.trimesh import TrimeshCookbook

logger = logging.getLogger(__file__)


class BaseCookbook(BaseModel, ABC):
    """
    The .from_data() and .from_file() class method also needs to be implemented, I did not make it an abstractmethod
    because each Cookbook has its own function signature.
    """

    class Config:
        arbitrary_types_allowed = True
        keep_untouched = (cached_property,)

    @property
    @abstractmethod
    def vertices_numpy_array(self) -> NDArrayFp64 | None:
        ...

    @property
    @abstractmethod
    def edges_numpy_array(self) -> NDArray | None:
        ...

    @property
    @abstractmethod
    def faces_numpy_array(self) -> NDArray | None:
        ...

    @property
    @abstractmethod
    def watertight(self) -> bool:
        """Check if a mesh is watertight, also known as manifold"""
        ...

    @abstractmethod
    def save(self, save_path: Path | str) -> None:
        ...

    def attempt_seal(self) -> Union["Cookbook", None]:
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

    def to_blender(self, name: str) -> "BlenderCookbook":
        from meshemy.cookbook.blender import BlenderCookbook

        if isinstance(self, BlenderCookbook):
            return self

        return BlenderCookbook.from_data(
            self.vertices_numpy_array, self.edges_numpy_array, self.faces_numpy_array, name
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


Cookbook = TypeVar("Cookbook", bound=BaseCookbook)
T = TypeVar("T")


class MeshIsObjectMixin(GenericModel, Generic[T]):
    mesh: T

    mesh_from_file_loader: ClassVar[Callable[[str], Any]] = ...

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_native(cls, mesh: T) -> "MeshIsObjectCookbook":
        return cls(mesh=mesh)

    @classmethod
    def from_file(cls, file_path: FilePath | str) -> "MeshIsObjectCookbook":
        return cls.from_native(mesh=cls.mesh_from_file_loader(str(file_path)))


MeshIsObjectCookbook = TypeVar("MeshIsObjectCookbook", bound=MeshIsObjectMixin)
