import os
from test import SAVE_TEST_PATH


def test_smoothen(open3d_cookbook):
    open3d_cookbook.smoothen(30)


# def test_seal(open3d_cookbook):
#     open3d_cookbook.attempt_seal_insurance()


def test_repair(open3d_cookbook):
    open3d_cookbook.repair()


def test_save(open3d_cookbook, ensure_test_save_file_is_deleted):
    open3d_cookbook.save(SAVE_TEST_PATH)
    assert SAVE_TEST_PATH.exists()
    os.remove(SAVE_TEST_PATH)
