import pytest

from pydotenvx.__main__ import main


def test_hello_no_file(capfd: pytest.CaptureFixture):
    main("run", ["--", "python", "tests/programs/hello_world.py"])
    output = capfd.readouterr()
    assert output.out == "Hello, world!\n"


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
def test_hello_some_files(capfd: pytest.CaptureFixture, dotenvs_names: list[int]):
    before = ["-f"]
    dotenvs = [f"tests/dotenvs/{x}.env" for x in dotenvs_names]
    after = ["--", "python", "tests/programs/hello_world.py"]
    args = before + dotenvs + after

    main("run", args)

    output = capfd.readouterr()
    assert output.out == "Hello, world!\n"
