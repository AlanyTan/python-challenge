"""generating test cases of problem:solution pairs

This should only be used for generating test_cases for non-function scripts.
For all function based .py code, they should use their own test_solution.py
"""

from utils.generate_problem_json import generate_problem_json, print_result


problem: dict = {
    "title": "assigning values to variables",
    "goal": "understanding variables and assignments",
    "description": """assign the specified values to the specified variables:
    assign integer 42 to variable a
    assign float 3.14 to variable b and c
    assign string 'words' to variable d
    assign byte b'bytes' to variable e
    assign boolean True to variable f and g
    assign None to variable h
    assign variable a to variable i"
    assign variable b to variable j and then assign a+j to k (try walrus)
""",
    "notes": "we provided a as an example, and b with a hint, and you will "
            "need to complete the rest yourself.",
    "starting_code": """# Assign integer 42 to variable a
a = 42
# Assign float 3.14 to variable b and c
b = c =
# Assign string 'words' to variable d

# Assign byte b'bytes' to variable e

# Assign boolean True to variable f and g

# Assign None to variable h

# Assign variable a to variable i

# Assign variable b to variable j and then assign a+j to k (use walrus operator)

""",
    "expected_output": ""
}
starting_condition = []


def solution() -> str:
    """the actual solution that will generate the expected output"""
    #from utils.generate_problem_json import print

    return print_result()


if __name__ == '__main__':
    generate_problem_json(__file__, problem, starting_condition, solution,
                          globals())
