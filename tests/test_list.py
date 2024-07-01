import pytest

from pydotenvx.__main__ import main


def test_list_no_file(capfd: pytest.CaptureFixture):
    main("list")
    output = capfd.readouterr()
    assert output.out == ""


@pytest.mark.parametrize(
    "path, expected_output",
    [
        pytest.param("tests/dotenvs/1.env", 'a="1"\nb="2"\nc="3"\n', id="1.env"),
        pytest.param("tests/dotenvs/2.env", 'd="44"\n', id="2.env"),
        pytest.param("tests/dotenvs/3.env", 'a="111"\n', id="3.env"),
    ],
)
def test_list_one_file(capfd: pytest.CaptureFixture, path, expected_output):
    main("list", ["-f", path])
    output = capfd.readouterr()
    assert output.out == expected_output


@pytest.mark.parametrize(
    "names, expected_output",
    [
        pytest.param(
            [1, 2, 3], "\n".join(['a="111"', 'b="2"', 'c="3"', 'd="44"\n']), id="1-2-3"
        ),
        pytest.param(
            [3, 2, 1], "\n".join(['a="1"', 'b="2"', 'c="3"', 'd="44"\n']), id="3-2-1"
        ),
    ],
)
def test_list_multi_files(capfd: pytest.CaptureFixture, names, expected_output):
    paths = [f"tests/dotenvs/{n}.env" for n in names]
    main("list", ["-f"] + paths)
    output = capfd.readouterr()
    assert output.out == expected_output
