"""generating test cases of problem:solution pairs

This should only be used for generating test_cases for non-function scripts.
For all function based .py code, they should use their own test_solution.py
"""

from utils.generate_problem_json import generate_problem_json, print_result


problem: dict = {
    "title": "literal values' types",
    "goal": "understanding the type of literals",
    "description": """put a literal of the specified type between each tape():
    an integer, and another integer
    a float, and another float 3.14
    a complex number
    a string, and a byte
    boolean True, and string 'True'
    None, and string 'None'
""",
    "notes": "i.e. print(type(1), type(2.71)) will output: "
            "<class 'int'> <class 'float'>",
    "starting_code": """\
print(type(), type())
print(type(), type())
print(type())
print(type(), type())
print(type(), type())
print(type(), type())
""",
    "expected_output": ""
}
starting_condition = []


def solution() -> str:
    """the actual solution that will generate the expected output"""
    from utils.generate_problem_json import print

    print(type(1), type(2))
    print(type(3.14), type(2.71))
    print(type(3 + 4j))
    print(type("words"), type(b"bytes"))
    print(type(True), type('False'))
    print(type(None), type('None'))

    return print_result()


if __name__ == '__main__':
    generate_problem_json(__file__, problem, starting_condition, solution,
                          globals())
