from typing import Optional
from typing import TYPE_CHECKING

from cleo.helpers import argument
from cleo.helpers import option
from cleo.io.outputs.output import Verbosity

from ..init import InitCommand
from ... import NullPrinter

if TYPE_CHECKING:
    from pkm_main.console.commands.show import ShowCommand


class DebugResolveCommand(InitCommand):

    name = "debug resolve"
    description = "Debugs dependency resolution."

    arguments = [
        argument("package", "The packages to resolve.", optional=True, multiple=True)
    ]
    options = [
        option(
            "extras",
            "E",
            "Extras to activate for the dependency.",
            flag=False,
            multiple=True,
        ),
        option("python", None, "Python version(s) to use for resolution.", flag=False),
        option("tree", None, "Display the dependency tree."),
        option("install", None, "Show what would be installed for the current system."),
    ]

    loggers = ["poetry.repositories.pypi_repository", "poetry.inspection.info"]

    def handle(self) -> Optional[int]:

        from pkm_buildsys.packages.project_package import ProjectPackage
        from pkm_main.factory import Factory
        from pkm_main.puzzle import Solver
        from pkm_main.repositories.pool import Pool
        from pkm_main.repositories.repository import Repository

        packages = self.argument("package")

        if not packages:
            package = self.poetry.package
        else:
            # Using current pool for determine_requirements()
            self._pool = self.poetry.pool

            package = ProjectPackage(
                self.poetry.package.name, self.poetry.package.version
            )

            # Silencing output
            verbosity = self.io.output.verbosity
            self.io.output.set_verbosity(Verbosity.QUIET)

            requirements = self._determine_requirements(packages)

            self.io.output.set_verbosity(verbosity)

            for constraint in requirements:
                name = constraint.pop("name")
                extras = []
                for extra in self.option("extras"):
                    if " " in extra:
                        extras += [e.strip() for e in extra.split(" ")]
                    else:
                        extras.append(extra)

                constraint["extras"] = extras

                package.add_dependency(Factory.create_dependency(name, constraint))

        package.python_versions = self.option("python") or (
            self.poetry.package.python_versions
        )

        env = self.poetry.env

        solver = Solver(self.poetry, Repository(), Repository(), package=package)

        ops = solver.solve().calculate_operations()

        self.line("")
        self.line("Resolution results:")
        self.line("")

        if self.option("tree"):
            show_command: ShowCommand = self.application.find("show")
            show_command.init_styles(self.io)

            packages = [op.package for op in ops]
            repo = Repository(packages)

            requires = package.all_requires
            for pkg in repo.packages:
                for require in requires:
                    if pkg.name == require.name:
                        show_command.display_package_tree(self.io, pkg, repo)
                        break

            return 0

        table = self.table([], style="compact")
        table.style.set_vertical_border_chars("", " ")
        rows = []

        if self.option("install"):
            pool = Pool()
            locked_repository = Repository()
            for op in ops:
                locked_repository.add_package(op.package)

            pool.add_repository(locked_repository)

            solver = Solver(self.poetry, Repository(), Repository(), printer=NullPrinter, package=package)
            with solver.use_environment(env):
                ops = solver.solve().calculate_operations()

        for op in ops:
            if self.option("install") and op.skipped:
                continue

            pkg = op.package
            row = [
                "<c1>{}</c1>".format(pkg.complete_name),
                "<b>{}</b>".format(pkg.version),
                "",
            ]

            if not pkg.marker.is_any():
                row[2] = str(pkg.marker)

            rows.append(row)

        table.set_rows(rows)
        table.render()
