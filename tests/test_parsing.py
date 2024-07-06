import pytest

from pydotenvx.__main__ import main


def test_strict_forbidden(capfd: pytest.CaptureFixture):
    status_code = main("list", ["-f", "tests/dotenvs/bad.env"])
    output = capfd.readouterr()
    assert output.out == ""
    assert status_code != 0
