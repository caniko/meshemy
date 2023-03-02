import os
from test import SAVE_TEST_PATH


def test_fix(pymesh_cookbook):
    pymesh_cookbook.fix()


def test_save(pymesh_cookbook, ensure_test_save_file_is_deleted):
    pymesh_cookbook.save(SAVE_TEST_PATH)
    assert SAVE_TEST_PATH.exists()
    os.remove(SAVE_TEST_PATH)
