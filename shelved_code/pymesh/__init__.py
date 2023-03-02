try:
    import pymesh
except ModuleNotFoundError as e:
    from meshemy.utility.exception import pymesh_module_not_installed_error

    pymesh_module_not_installed_error(e)

from meshemy.pymesh.fix_mesh import pymesh_fix_mesh
