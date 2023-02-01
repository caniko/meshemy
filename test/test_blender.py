

def test_planar_decimation(blender_cookbook):
    blender_cookbook.planar_decimate(1.0)


def test_merge_close(blender_cookbook):
    blender_cookbook.merge_close(5.0)


def test_to_o3d(blender_cookbook):
    assert blender_cookbook.to_o3d()
