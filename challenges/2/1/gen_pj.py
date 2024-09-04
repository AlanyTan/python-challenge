"""generating test cases of problem:solution pairs

This should only be used for generating test_cases for non-function scripts.
For all function based .py code, they should use their own test_solution.py
"""

import os
import json
from config import config


problem: dict = {
    "title": "output literal values",
    "goal": "use print() to output literal values",
    "description": "Output the following values using print() function:\n"
            "real numbers 3, 3.14\n"
            "a complex number 3 + 4j\n"
            "string 'words', and byte b'bytes'\n"
            "True, and False"
            "None",
    "notes": "print can take multiple arguments like print(1,2), will print:"
            "1 2",
    "starting_code": "print(,)\nprint()\nprint(,)\nprint(,)\n,print()\n",
    "expected_output": ""
}
starting_condition = [""]


def solution() -> str:
    """the actual solution that will generate the expected output"""
    from utils.generate_problem_json import print, print_result

    print(3, 3.14)
    print(3 + 4j)
    print("words", b"bytes")
    print(True, False)
    print(None)

    return print_result()


def generate_problem_json(fn: str) -> None:
    """generate the problem.json file for the challenge"""
    my_dir = os.path.dirname(os.path.abspath(fn))
    problem_json = os.path.join(my_dir, config.PROBLEM_FILENAME)
    exec(starting_condition[0], None, None)
    problem["expected_output"] = solution()
    test_cases = []
    for sc in starting_condition[1:]:
        for o in [o for o in globals() if not o.startswith("__")]:
            del globals()[o]
        for o in [o for o in locals() if not o.startswith("__")]:
            del locals()[o]
        exec(sc, None, None)
        expected_output = solution()
        test_cases.append((sc, expected_output))
    problem["test_cases"] = test_cases

    with open(problem_json, 'w', encoding='utf-8') as f:
        json.dump(problem, f, indent=4)


if __name__ == '__main__':
    generate_problem_json(__file__)
