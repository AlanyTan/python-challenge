"""generating test cases of problem:solution pairs

This should only be used for generating test_cases for non-function scripts.
For all function based .py code, they should use their own test_solution.py
"""

import os
import json
from config import config


problem: dict = {
    "title": "output literal values",
    "goal": "understanding the type of literals",
    "description": "put a literal of the specified type between each tape():\n"
            "an integer, and another integer"
            "a float, and another float 3.14\n"
            "a complex number \n"
            "a string, and a byte\n"
            "boolean True, and string 'True'"
            "None, and string 'None'",
    "notes": "i.e. print(type(1), type(2.71)) will output: "
            "<class 'int'> <class 'float'>",
    "starting_code": """print(type(), type())
print(type(), type())
print(type())
print(type(), type())
print(type(), type())
print(type(), type())
""",
    "expected_output": ""
}
starting_condition = [""]


def solution() -> str:
    """the actual solution that will generate the expected output"""
    from utils.generate_problem_json import print, print_result

    print(type(1), type(2))
    print(type(3.14), type(2.71))
    print(type(3 + 4j))
    print(type("words"), type(b"bytes"))
    print(type(True), type('False'))
    print(type(None), type('None'))

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
