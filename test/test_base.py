import os
from test import SAVE_TEST_PATH

import pytest

from meshemy.cookbook.base import BaseCookbook


def _dynamic_fixture(request, cookbook_fixture: str) -> BaseCookbook:
    return request.getfixturevalue(cookbook_fixture)


@pytest.mark.parametrize("cookbook_fixture", ["blender_cookbook", "open3d_cookbook", "trimesh_cookbook"])
def test_save(cookbook_fixture: str, ensure_test_save_file_is_deleted, request):
    cookbook = _dynamic_fixture(request, cookbook_fixture)

    cookbook.save(SAVE_TEST_PATH)
    assert SAVE_TEST_PATH.exists()

    os.remove(SAVE_TEST_PATH)


@pytest.mark.parametrize("cookbook_fixture", ["blender_cookbook", "open3d_cookbook", "trimesh_cookbook"])
def test_watertight(cookbook_fixture: str, request):
    assert not _dynamic_fixture(request, cookbook_fixture).watertight
