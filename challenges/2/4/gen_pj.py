"""generating test cases of problem:solution pairs

This should only be used for generating test_cases for non-function scripts.
For all function based .py code, they should use their own test_solution.py

Usage:
    pythong -m challenge.id.gen_pj.py
"""

import os
import json
from config import config


problem: dict = {
    "title": "logical operations and short circuit",
    "goal": "understanding the logical values, Truthy, Falsy, and operations "
            "and short circuit",
    "description": """This challenge will require you to complete the following\
code by adding 
your answers to the right side of the = on the lines started with answer_,
 i.e.:
answer_is_a_bool_type = False  # because a is int type
answer_a_and_b_is_of_type = 'float'  # because a is Truthy, b is Falsy, 
# so, and  returns the value of b (0.0) which is of type float
""",
    "notes": "when answering a type question use quotation marks i.e. 'int'; "
            "it is expected that running this program does not produce any output.",
    "condition_code": """\
a = 1
b = 0.0
c = '0'
d = ''
e = True
f = 'False'
g = None
""",
    "starting_code": """\
# given the above values of variable a to g, complete the assignment 
#   statements started with answer_ by adding the actual answer:

# assign either True or False to the answer_ variablers below about a and (not a)
answer_is_a_bool_type = 
answer_is_not_a_bool_type = 

# assign either True or False to the answer_ variables below about b, c, d, e and f
answer_is_b_Truthy = 
answer_is_c_Truthy = 
answer_is_d_Truthy = 
answer_is_e_Truthy = 
answer_is_f_Truthy = 
answer_is_g_Truthy = 

# assign the data type to the following answer_ variables 
# possible answers are 'int', 'float', 'str', 'bool', 'None'
a_and_b = a and b
answer_a_and_b_is_of_type = 

b_or_c = b or c
answer_b_or_c_is_of_type = 

not_d_or_2e = not d or e * 2
answer_not_d_or_2e_is_of_type = 

f_and_not_g = f and not g
answer_f_and_not_g_is_of_type = 

b_or_not_d_and_2e = b or not d and e * 2
answer_b_or_not_d_and_2e_is_of_type = 
""",
    "expected_output": ""
}
starting_condition = [""]


def solution() -> str:
    """the actual solution that will generate the expected output"""

    return ""


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
