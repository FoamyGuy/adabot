# SPDX-FileCopyrightText: 2021 Michael Schroeder
#
# SPDX-License-Identifier: MIT

"""Integration tests for 'adabot/circuitpython_libraries.py'"""

import pytest  # pylint: disable=unused-import

from adabot.lib import common_funcs
from adabot import github_requests
from adabot import circuitpython_libraries

from adabot.lib import circuitpython_library_validators

# pylint: disable=unused-argument
def mock_list_repos(*args, **kwargs):
    """Function to monkeypatch `common_funcs.list_repos()` for a shorter set of repos."""
    return [
        github_requests.get("/repos/adafruit/Adafruit_CircuitPython_TestRepo").json()
    ]


def test_circuitpython_libraries(monkeypatch, pytestconfig):
    """Test main function of 'circuitpyton_libraries.py', without writing an output file."""

    monkeypatch.setattr(common_funcs, "list_repos", mock_list_repos)

    # Delete specific tests that require repository secrets
    # They can't be tested via, so let's remove them and test the others
    if not pytestconfig.getoption("--use-tokens"):
        print("FDSFSD")
        for funcname in circuitpython_library_validators.TOKEN_FUNCTIONS:
            monkeypatch.delattr(circuitpython_library_validators.LibraryValidator, funcname)

    circuitpython_libraries.main(validator="all")


# pylint: disable=invalid-name
def test_circuitpython_libraries_output_file(monkeypatch, pytestconfig, tmp_path, capsys):
    """Test main funciton of 'circuitpython_libraries.py', with writing an output file."""

    monkeypatch.setattr(common_funcs, "list_repos", mock_list_repos)

    # Delete specific tests that require repository secrets
    # They can't be tested via, so let's remove them and test the others
    if not pytestconfig.getoption("--use-tokens"):
        for funcname  in circuitpython_library_validators.TOKEN_FUNCTIONS:
            monkeypatch.delattr(circuitpython_library_validators.LibraryValidator, funcname)

    tmp_output_file = tmp_path / "output_test.txt"

    circuitpython_libraries.main(validator="all", output_file=tmp_output_file)

    captured = capsys.readouterr()

    assert tmp_output_file.read_text() == captured.out
