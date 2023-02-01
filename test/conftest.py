import os

import pytest

from meshemy.cookbook.blender import BlenderCookbook
from meshemy.cookbook.open3d import Open3dCookbook
from test import GLB_MESH_PATH, SAVE_TEST_PATH


@pytest.fixture(scope="function")
def blender_cookbook():
    return BlenderCookbook.from_file(GLB_MESH_PATH, "monkey")


@pytest.fixture(scope="function")
def open3d_cookbook():
    return Open3dCookbook.from_file(GLB_MESH_PATH)


@pytest.fixture(scope="function")
def ensure_test_save_file_is_deleted():
    if SAVE_TEST_PATH.exists():
        os.remove(SAVE_TEST_PATH)
