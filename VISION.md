# Meshemy vision

Meshemy is a Python toolbelt for manipulating mesh. It consolidates several
mesh backends — Blender, Open3D, and Trimesh — behind "cookbook" classes that
share an operation vocabulary and can convert between each other, so a script
picks the backend that has the operation it needs instead of surrendering to
one library's API. Backends are optional extras; `full` installs all of them.

## Problem

Mesh processing in Python is split across libraries with incompatible object
models. Decimation, smoothing, repair, sealing, and containment each exist in
some backends and not others, and moving a mesh between them is manual glue.
Blender adds its own scripting environment, where mode transitions and empty
scenes are easy to get wrong. Repeating that glue in every project hides the
part that actually matters: the mesh operation.

## Principles

- **One cookbook per backend, same operations where supported.** `BlenderCookbook`,
  `Open3dCookbook`, and `TrimeshCookbook` expose the same shape of calls.
- **Conversion instead of lock-in.** Cookbooks convert to one another
  (`.to_o3d()`, for example) rather than forcing a single backend on the user.
- **Optional, explicit dependencies.** Each backend is an extra, and the default
  Open3D dependency is `open3d-cpu` because the library does not need a GPU.
- **Experiments stay out of the package.** `shelved_code/` holds abandoned work
  such as the old pymesh code without shipping it.

## Scope

- cookbook classes for Blender, Open3D, and Trimesh
- mesh operations: decimation, smoothing, repair, sealing, transforms
- conversion between cookbooks
- Blender scene and workflow helpers
- test suite exercising all three backends

Python 3.11 is the supported interpreter, and the Blender extra targets Blender
4.2 LTS.

## Place in the fleet

`mask_to_mesh` depends on `meshemy[full,open3d]` from its `pyproject.toml`, using
it as the mesh backend for meshes generated from segmentation masks.
