"""utility tools to be used by tests"""
from typing import Callable
import json
import os
import pytest
from config import config
from .common import challenge_details


def py_param_id_format_factory() -> Callable[..., str]:
    """Factory function to create a closure for id_format.

    >>> id_format = py_param_id_format_factory()
    >>> id_format("ABC")
    'Condition:\\nABC'
    >>> id_format("123")
    'Expected:\\n123'
    """
    is_key = True

    def id_format(arg) -> str:
        """Format the argument based on whether it's a key or value."""
        nonlocal is_key  # Use nonlocal to modify the enclosed variable
        if is_key:
            is_key = False
            return f"Condition:\n{arg}"
        else:
            is_key = True
            return f"Expected:\n{arg}"

    return id_format


if __name__ == '__main__':
    import doctest
    doctest.testmod()


id_format = py_param_id_format_factory()  # Create an instance of the closure


@pytest.fixture(scope="module")
def challenge_data(request: pytest.FixtureRequest) -> dict:
    """fixture to read challenge_data from problem.json"""
    challenge_data = challenge_details(str(
        request.config.getoption("--challenge_id")))
    return challenge_data


@pytest.fixture(scope="module")
def code_submitted(request: pytest.FixtureRequest) -> str:
    """fixture to read user submitted code"""
    user_file: str = str(request.config.getoption("--user_file"))
    with open(user_file, "rt", encoding='utf-8') as uf:
        code_submitted = uf.read()
    return code_submitted


def pytest_generate_tests(metafunc):
    """pytest hook used to generate testcases dynamically """
    test_cases = []
    challenge_data = challenge_details(str(
        metafunc.config.getoption("--challenge_id")))
    test_cases.append((challenge_data.get("starting_code", ''),
                      challenge_data.get("expected_output", '')))
    test_cases.extend(challenge_data.get("test_cases", []))
    metafunc.parametrize("start_condition, expected_output", test_cases,
                         ids=id_format)


def test_solution(challenge_data: dict, code_submitted: str,
                  start_condition: str, expected_output: str,
                  capsys) -> None:
    """run the user submitted code to test it.

    Usage:
        pytest test_solution -qq -rN -tb=short --user_file=submissions/u1/1.py
    """

    starting_code = challenge_data.get("starting_code", '')

    code_to_test = code_submitted.replace(starting_code, start_condition)

    exec(code_to_test, None, None)
    captured = capsys.readouterr()
    received_output = captured.out.strip()

    expected_output = f"{expected_output}"

    assert received_output == expected_output
