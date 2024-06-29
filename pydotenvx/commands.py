from __future__ import annotations

from typing import Type


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
    def create_from_cli_params(args: list[str]) -> Command:
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()


class ListCommand(Command):
    def __init__(self, dotenv_paths: list[str]):
        self.dotenv_paths = dotenv_paths

    @staticmethod
    def create_from_cli_params(args: list[str]) -> ListCommand:
        if len(args) == 0:
            raise ValueError("No parameters for list command.")

        arg_0 = args[0]
        if arg_0 != "-f":
            raise ValueError(
                f"Expected 1st parameter to be the '-f' flag, but got: {arg_0}"
            )

        return ListCommand(dotenv_paths=args[1:])

    def run(self):
        vars = {}
        for dotenv_path in self.dotenv_paths:
            vars.update(_load_dotenv_file(dotenv_path))

        for k, v in vars.items():
            print(f"{k}={v}")


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
_names_to_classes = {"list": ListCommand}
