try:
    # noinspection PyCompatibility
    import importlib.metadata as mtd
except ModuleNotFoundError:
    import importlib_metadata as mtd

try:
    __version__ = mtd.version("pkm_main")
except mtd.PackageNotFoundError as e:
    from pathlib import Path
    from pkm_buildsys.pyproject.project import Project

    __version__ = Project.read(Path(__file__).parent / "../pyproject.toml").version
