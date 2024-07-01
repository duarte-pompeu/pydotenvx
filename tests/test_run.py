import subprocess

import pytest


def test_hello_no_file():
    result = subprocess.run(
        [
            "python",
            "-m",
            "pydotenvx",
            "run",
            "--",
            "python",
            "tests/programs/hello_world.py",
        ]
    )
    assert result.returncode == 0


@pytest.mark.parametrize(
    "dotenvs_names",
    # TODO: use itertools for this?
    [
        [1],
        [2],
        [3],
        [1, 1],
        [1, 2],
        [1, 3],
        [2, 1],
        [2, 2],
        [2, 3],
        [3, 1],
        [3, 2],
        [3, 3],
        [1, 1, 1],
        [1, 2, 1],
        [1, 2, 2],
        [1, 2, 3],
        [1, 3, 1],
        [1, 3, 2],
        [1, 3, 3],
        [2, 1, 1],
        [2, 1, 2],
        [2, 2, 1],
        [2, 2, 2],
        [2, 3, 1],
        [2, 3, 2],
        [2, 3, 3],
        [3, 1, 1],
        [3, 1, 2],
        [3, 1, 3],
        [3, 2, 1],
        [3, 2, 2],
        [3, 2, 3],
        [3, 3, 1],
        [3, 3, 2],
        [3, 3, 3],
    ],
)
def test_hello_some_files(dotenvs_names):
    before = ["python", "-m", "pydotenvx", "run", "-f"]
    after = ["--", "python", "tests/programs/hello_world.py"]
    dotenvs = [f"tests/dotenvs/{x}.env" for x in dotenvs_names]
    commands = before + dotenvs + after
    result = subprocess.run(commands)
    assert result.returncode == 0
