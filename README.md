# Meshemy: Python toolbelt for manipulating mesh
Consolidation package for manipulating mesh. Comes with cookbook models from each package

## Installation
```shell
pip install meshemy[full]
```
Use it in your poetry package
```shell
poetry add meshemy -E full
```

## Usage
You need to pick at least one extra for this package to be useful. Install all modules by installing `full`.

### Cookbook
Currently, Blender, Open3D, and Trimesh is supported.

#### Blender
The `blender` extra must be installed.
```python
from meshemy.cookbook.blender import BlenderCookbook

blender_cook = BlenderCookbook.from_file("path_to_mesh.<any_format>")
blender_cook.planar_decimate(degree_tol=5.0)
```
You can convert to any other cookbook `.to_o3d()`, for instance.

#### Open3D
The `open3d` extra must be installed.
```python
from meshemy.cookbook.open3d import Open3dCookbook

o3d_cook = Open3dCookbook.from_file("path_to_mesh.<any_format>")
o3d_cook.smoothen(5)
o3d_cook.repair()
```

#### Open3D
The `trimesh` extra must be installed.
```python
from meshemy.cookbook.trimesh import TrimeshCookbook

trimesh_cook = TrimeshCookbook.from_file("path_to_mesh.<any_format>")
trimesh_cook.contains(vertices)
```

### More
For more information, look at the source code, it is relatively easy to read. Start in the `cookbook` submodule.