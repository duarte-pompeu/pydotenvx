from __future__ import annotations

import os
from subprocess import Popen
from typing import Any, Type


def find_command_class(cmd_name: str) -> Type[Command]:
    try:
        CommandClass = _names_to_classes[cmd_name]
        return CommandClass

    except KeyError as err:
        expected_names = list(_names_to_classes.keys())
        raise ValueError(
            f"Expected command to be one of {expected_names}, but got: {cmd_name}"
        ) from err


class Command:
    @staticmethod
    def create_from_cli_params(args: list[str] | None = None) -> Command:
        raise NotImplementedError()

    def run(self) -> int | Any:
        raise NotImplementedError()


class ListCommand(Command):
    def __init__(self, dotenv_paths: list[str]):
        self.dotenv_paths = dotenv_paths

    @staticmethod
    def create_from_cli_params(args: list[str] | None = None) -> ListCommand:
        if args is None:
            args = []

        if len(args) == 0:
            dotenv_paths = []
        else:
            arg_0 = args[0]
            if arg_0 != "-f":
                raise ValueError(
                    f"Expected 1st parameter to be the '-f' flag, but got: {arg_0}"
                )
            dotenv_paths = args[1:]

        return ListCommand(dotenv_paths=dotenv_paths)

    def run(self) -> int | Any:
        vars = {}
        for dotenv_path in self.dotenv_paths:
            vars.update(_load_dotenv_file(dotenv_path))

        for k, v in sorted(vars.items()):
            print(f'{k}="{v}"')

        return 0


class RunCommand(Command):
    def __init__(self, cmd, cmd_args, dotenv_paths: list[str] | None = None):
        if dotenv_paths is None:
            dotenv_paths = []

        self.cmd = cmd
        self.cmd_args = cmd_args
        self.dotenv_paths = dotenv_paths

    @staticmethod
    def create_from_cli_params(args: list[str] | None = None) -> RunCommand:
        if args is None:
            args = []

        dotenv_args: list[str] = []
        subprocess = ""
        subprocess_args: list[str] = []

        for i, arg in enumerate(args):
            # let's use -- to split between dotenv args and subprocess args:
            # POSIX.1-2017
            # 12.2 Utility Syntax Guidelines
            # Guideline 10:
            # The first -- argument that is not an option-argument should be accepted as a delimiter indicating the end of options.
            # Any following arguments should be treated as operands, even if they begin with the '-' character.
            if arg == "--":
                break
            dotenv_args.append(arg)

        subprocess = args[i + 1]

        for arg in args[i + 2 :]:
            subprocess_args.append(arg)

        if len(dotenv_args) == 0:
            dotenv_paths = []
        else:
            dotenv_arg_0 = dotenv_args[0]
            if dotenv_arg_0 != "-f":
                raise ValueError(
                    f"Expected 1st parameter to be the '-f' flag, but got: {dotenv_arg_0}"
                )
            dotenv_paths = dotenv_args[1:]

        return RunCommand(subprocess, subprocess_args, dotenv_paths)

    def run(self) -> int | Any:
        vars = {}
        for dotenv_path in self.dotenv_paths:
            vars.update(_load_dotenv_file(dotenv_path))

        cmd_env = os.environ.copy()
        cmd_env.update(vars)

        command = [self.cmd] + self.cmd_args
        p = Popen(command, universal_newlines=True, bufsize=0, shell=False, env=cmd_env)
        _, _ = p.communicate()

        return p.returncode


# TODO: allow to load multiple paths from this
# TODO: validate all paths are ok
def _load_dotenv_file(path: str) -> dict:
    vars = {}
    with open(path) as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue

            key, value = line.split("=")
            vars[key] = value

    return vars


# TODO: use factory and decorators
_names_to_classes = {"list": ListCommand, "run": RunCommand}
