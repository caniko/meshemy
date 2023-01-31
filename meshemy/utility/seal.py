import pymeshfix
from pydantic_numpy import NDArray


def seal_mesh(vertices: NDArray, faces: NDArray) -> tuple[NDArray, NDArray]:
    return pymeshfix.clean_from_arrays(vertices, faces, joincomp=True, verbose=False)
