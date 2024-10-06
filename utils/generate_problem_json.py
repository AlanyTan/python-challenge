"""utility tools used by code to generate problem.json"""
import json
import os
from typing import Callable
from config import config

temp_result = []

original_print = print


def print(*args, **kwargs) -> None:
    """shadow the built-in print function"""
    if "end" in kwargs:
        new_line = kwargs["end"]
    else:
        new_line = "\n"

    if "sep" in kwargs:
        sep = kwargs["sep"]
    else:
        sep = " "

    temp_result.append(sep.join(map(str, args)) + new_line)


def print_result() -> str:
    """return final print result as a single string"""
    return "".join(temp_result)


def cleanup_result() -> None:
    """empty the temp_result list (prepare for a clean run)"""
    temp_result.clear()


def generate_problem_json(fn: str, problem: dict, starting_condition: list,
                          solution: Callable, global_scope: dict) -> None:
    """generate the problem.json file for the challenge

    A problem is expected to have "condition_code" that the user should not 
        change, which is used to set up running conditions; this function will
        first use "condition_code" code to setup initial run, and generate 
        content for "expected_output" key of problem;
        It then checks to see if starting_condition is Truthy, if so, it
        iterates through each member of starting_condition,  and use it  to 
        replace "condition_code" as starting condition and re-run the solution 
        function to generate a new set of expected_output; it then uses the 
        start_condition member and its corresponding output to form a tuple
        and append it to "test_cases" list of the problem object.
    After all start_condition have been processed this way, it writes the 
        problem object to the problem.json file in the same dir as provided by 
        the parameter fn)

    Args:
        fn: file_name of the current gen_pj.py
        problem: the problem dict that will be mutated and written to problem.json
        starting_condition: list of replacement starting condition code
        solution: the function that simulates the solution use given condition
                    to generate expected outcome
        global_scope: the global object for the solution 

    Returns: 
        None, the updated problem dict will be writtent to os.path.join(
          os.path.dirname(fn),config.PROBLEM_FILE)

    Usage:
        >>>generate_problem_json(__file__, problem, starting_condition, 
                                solution, globals())

    """
    my_dir = os.path.dirname(os.path.abspath(fn))
    problem_json = os.path.join(my_dir, config.PROBLEM_FILENAME)
    cleanup_result()
    exec(problem.get('condition_code', ""), global_scope)
    problem["expected_output"] = solution()
    test_cases = []
    for sc in starting_condition:
        exec(sc, global_scope)
        cleanup_result()
        expected_output = solution()
        test_cases.append((sc, expected_output))
    problem["test_cases"] = test_cases

    with open(problem_json, 'w', encoding='utf-8') as f:
        json.dump(problem, f, indent=4)


if __name__ == '__main__':
    print(1, "str", False)
    original_print(print_result())
