import pytest

from pydotenvx.__main__ import main


def test_comments_ok(capfd: pytest.CaptureFixture):
    status_code = main("list", ["-f", "tests/dotenvs/valid/comments.env"])
    output = capfd.readouterr()
    print(output.err)
    assert status_code == 0
    assert output.out == 'x="1"\ny="2"\nz="3"\n'


def test_empty_ok(capfd: pytest.CaptureFixture):
    status_code = main("list", ["-f", "tests/dotenvs/valid/empty.env"])
    output = capfd.readouterr()
    print(output.err)
    assert status_code == 0
    assert output.out == ""


def test_escaped_quotes(capfd: pytest.CaptureFixture):
    status_code = main("list", ["-f", "tests/dotenvs/valid/escaping.env"])
    output = capfd.readouterr()
    print(output.err)
    assert status_code == 0
    assert output.out == """a=\nb="2"\nc="\n"""


def test_no_file_fail(capfd: pytest.CaptureFixture):
    status_code = main("list", ["-f", "2d538df1-5380-4f46-b962-38990d7e9b55.env"])
    output = capfd.readouterr()
    assert status_code != 0
    assert output.out == ""


def test_no_quotes_fail(capfd: pytest.CaptureFixture):
    status_code = main("list", ["-f", "tests/dotenvs/invalid/bad.env"])
    output = capfd.readouterr()
    assert status_code != 0
    assert output.out == ""


def test_spacing_ok(capfd: pytest.CaptureFixture):
    status_code = main("list", ["-f", "tests/dotenvs/valid/spacing.env"])
    output = capfd.readouterr()
    print(output.err)
    assert status_code == 0
    assert output.out == """a="1111"\nb="2222"\nc="3333"\nd="4444"\n"""
