from pathlib import Path

from poetry.core.pyproject.profiles import ProfilesActivationRequest
from poetry.core.pyproject.project import Project
from poetry.factory import Factory

from .command import Command


class CheckCommand(Command):
    name = "check"
    description = "Checks the validity of the <comment>pyproject.toml</comment> file."

    def handle(self) -> int:
        # Load poetry config and display errors, if any
        poetry_file = Factory.locate(Path.cwd())
        config = Project.read(poetry_file, ProfilesActivationRequest.from_commandline("check", [])).poetry_config
        check_result = Factory.validate(config, strict=True)
        if not check_result["errors"] and not check_result["warnings"]:
            self.info("All set!")

            return 0

        for error in check_result["errors"]:
            self.line("<error>Error: {}</error>".format(error))

        for error in check_result["warnings"]:
            self.line("<warning>Warning: {}</warning>".format(error))

        return 1
