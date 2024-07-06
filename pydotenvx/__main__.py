import logging
import sys

from pydotenvx.commands import find_command_class


def main(command, args: list[str] | None = None) -> int:
    if args is None:
        args = []

    try:
        CmdClass = find_command_class(command)
        command = CmdClass.create_from_cli_params(args)
        command.run()
        return 0
    except Exception as err:
        logging.error(err)
        return -1


def script():
    dotenv_command = sys.argv[1]
    cli_args = sys.argv[2:]
    code = main(dotenv_command, cli_args)
    sys.exit(code)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    script()
