import logging
import sys

from pydotenvx.commands import find_command_class

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    dotenv_args: list[str] = []
    subprocess_args: list[str] = []

    arg_reference = dotenv_args
    for arg in sys.argv[1:]:
        if arg == "--":
            arg_reference = subprocess_args
            continue
        arg_reference.append(arg)

    cmd, args = dotenv_args[0], dotenv_args[1:]

    logging.debug(cmd)
    logging.debug(args)
    logging.debug(subprocess_args)

    CmdClass = find_command_class(cmd)
    command = CmdClass.create_from_cli_params(args)
    command.run()
