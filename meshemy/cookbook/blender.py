import logging
from typing import Optional, Sequence

import bpy
import numpy as np
import open3d as o3d
from pydantic import BaseModel, FilePath

from meshemy.blender.constant import SUFFIX_TO_READER, SUFFIX_TO_WRITER
from meshemy.blender.shortcut.io import load_mesh_into_object
from meshemy.blender.shortcut.select import latest_mesh, select_object
from meshemy.blender.utils import (
    load_mesh_from_o3d,
    vertices_and_faces,
)
from meshemy.blender.workflows import merge_close, planar_decimate_mesh
from meshemy.cookbook.open3d import Open3dCookbook
from meshemy.utility.io import o3d_from_vertices_faces
from meshemy.utility.seal import seal_mesh


logger = logging.getLogger(__file__)


class BlenderCookbook(BaseModel):
    mesh_name: str

    def planar_decimate(self, degree_tol: float) -> None:
        planar_decimate_mesh(degree_tol, mesh_object_name=self.mesh_name)
        logger.debug(f"Planar decimation on {self.mesh_name}, degree tolerance {degree_tol}")

    def merge_close(self, distance_tol: float) -> None:
        merge_close(distance_tol, mesh_object_name=self.mesh_name)
        logger.debug(f"Merging proximal vertices on {self.mesh_name}, distance tolerance {distance_tol}")

    def save(self, path: FilePath) -> None:
        _ob = select_object(self.mesh_name)
        SUFFIX_TO_WRITER[path.suffix](filepath=str(path))

    def to_o3d(self, attempt_seal_insurance: bool = False) -> Open3dCookbook:
        vertices, faces = vertices_and_faces(mesh_object_name=self.mesh_name)
        if attempt_seal_insurance:
            vertices, faces = seal_mesh(vertices, faces)
        return Open3dCookbook(mesh=o3d_from_vertices_faces(vertices, faces))

    @classmethod
    def from_data(
        cls,
        name: str,
        vertices: Sequence,
        edges: Optional[Sequence],
        faces: Optional[Sequence],
    ) -> "BlenderCookbook":
        assert edges is not None or faces is not None

        mesh = bpy.data.meshes.new(f"{name}_mesh")
        mesh.from_pydata(
            np.asarray(vertices),
            np.asarray(edges) if edges is not None else None,
            np.asarray(faces) if faces is not None else None,
        )
        mesh.update()

        load_mesh_into_object(name, mesh)

        return cls(mesh_name=name)

    @classmethod
    def from_o3d(cls, mesh: o3d.geometry.TriangleMesh, name: str) -> "BlenderCookbook":
        _ob = load_mesh_from_o3d(mesh, name)
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
