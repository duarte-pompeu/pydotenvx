import logging
import sys

from pydotenvx.commands import find_command_class


def main(*args):
    CmdClass = find_command_class(dotenv_command)
    command = CmdClass.create_from_cli_params(cli_args)
    command.run()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    dotenv_command = sys.argv[1]
    cli_args = sys.argv[2:]
    main(cli_args)
