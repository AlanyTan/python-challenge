"""generating test cases of problem:solution pairs"""

from utils.generate_problem_json import generate_problem_json, print_result

problem: dict = {
    "title": "output literal values",
    "goal": "use print() to output literal values",
    "description": """Output the following values using print() function:
    real numbers 3, 3.14
    a complex number 3 + 4j
    string 'words', and byte b'bytes'
    True, and False
    None
""",
    "notes": "print can take multiple arguments like print(1,2), will print:"
            "1 2",
    "starting_code": """\
print(,)
print()
print(,)
print(,)
print()
""",
    "expected_output": ""
}
starting_condition = []


def solution() -> str:
    """the actual solution that will generate the expected output"""
    from utils.generate_problem_json import print

    print(3, 3.14)
    print(3 + 4j)
    print("words", b"bytes")
    print(True, False)
    print(None)

    return print_result()


if __name__ == '__main__':
    generate_problem_json(__file__, problem, starting_condition, solution,
                          globals())
