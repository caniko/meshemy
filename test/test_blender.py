import os
from test import SAVE_TEST_PATH


def test_planar_decimation(blender_cookbook):
    blender_cookbook.planar_decimate(1.0)


def test_merge_close(blender_cookbook):
    blender_cookbook.merge_close(5.0)


def test_to_o3d(blender_cookbook):
    assert blender_cookbook.to_o3d()


def test_save(blender_cookbook, ensure_test_save_file_is_deleted):
    blender_cookbook.save(SAVE_TEST_PATH)
    assert SAVE_TEST_PATH.exists()
    os.remove(SAVE_TEST_PATH)
