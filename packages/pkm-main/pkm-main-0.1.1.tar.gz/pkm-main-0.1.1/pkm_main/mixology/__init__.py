from typing import Dict
from typing import List
from typing import TYPE_CHECKING

from .version_solver import VersionSolver

if TYPE_CHECKING:
    from pkm_buildsys.packages.project_package import ProjectPackage
    from pkm_main.packages import DependencyPackage
    from pkm_main.puzzle.provider import Provider

    from .result import SolverResult


def resolve_version(
        root: "ProjectPackage",
        provider: "Provider",
        locked: Dict[str, "DependencyPackage"] = None,
        use_latest: List[str] = None,
) -> "SolverResult":
    solver = VersionSolver(root, provider, locked=locked, use_latest=use_latest)

    return solver.solve()
