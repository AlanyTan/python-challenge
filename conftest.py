"""configuration file for pytest"""

import pytest
from pytest import FixtureRequest


@pytest.fixture
def user_file(request: FixtureRequest):
    """return commandline option value of --user_file"""
    return request.config.getoption("--user_file")


@pytest.fixture
def challenge_id(request: FixtureRequest) -> str:
    """return commandline option value of --challenge_id"""
    return str(request.config.getoption("--challenge_id"))


def pytest_addoption(parser) -> None:
    """setup pytest to accept command line options --user_file"""
    parser.addoption("--user_file", action="store", default="",
                     help="the file name of the user submitted solution")
    parser.addoption("--challenge_id", action="store", default="",
                     help="the challenge_id of the challenge to test")


# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     """Modify terminal summary report to hide summary info."""
#     terminalreporter.stats = {}  # This effectively clears the summary
