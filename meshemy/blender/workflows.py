from typing import Optional

import bpy
import numpy as np

from meshemy.blender.shortcut.select import (
    get_object_by_name,
    select_one_or_all,
    set_object_active_by_name,
)
from meshemy.blender.utils import safely_enter_mode


def planar_decimate_mesh(degrees: float = 1.0, mesh_object_name: Optional[str] = None) -> None:
    if mesh_object_name:
        obj = set_object_active_by_name(mesh_object_name)

    safely_enter_mode("OBJECT")

    bpy.ops.object.modifier_add(type="DECIMATE")
    obj.modifiers["Decimate"].decimate_type = "DISSOLVE"
    obj.modifiers["Decimate"].angle_limit = np.deg2rad(degrees)

    bpy.ops.object.modifier_apply(modifier="Decimate")


def merge_close(tolerance: float = 0.01, mesh_object_name: Optional[str] = None) -> None:
    select_one_or_all(mesh_object_name)

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.remove_doubles(threshold=tolerance)


def add_simple_material(mesh_name: str, color: tuple[float, float, float, float]) -> None:
    mesh_object = get_object_by_name(mesh_name)

    # Create a new material
    material = bpy.data.materials.new(name=f"{mesh_name}_material")

    # Enable 'Use Nodes' for the material
    material.use_nodes = True

    # Access the material's node tree
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Clear existing nodes
    nodes.clear()

    # Create Principled BSDF shader node
    shader_node = nodes.new(type="ShaderNodeBsdfPrincipled")
    shader_node.location = (0, 0)

    # Set the color of the shader node. Define the color as an RGBA tuple (red, green, blue, alpha)
    shader_node.inputs["Base Color"].default_value = color

    # Create Output node
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    output_node.location = (300, 0)

    # Link the shader node to the output node
    links.new(shader_node.outputs["BSDF"], output_node.inputs["Surface"])

    if mesh_object is not None:
        # Add the material to the mesh object
        if mesh_object.data.materials:
            mesh_object.data.materials[0] = material
        else:
            mesh_object.data.materials.append(material)
    else:
        print(f"No object named '{mesh_name}' found in the scene.")
