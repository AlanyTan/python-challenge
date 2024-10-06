"""module to run user submission and check the outcome matches expected"""

import re
import json
import os
import subprocess
import sys
from config import config


def execute_script(file_to_test: str = '') -> str:
    """execute Python script file, and return the output/error.

    >>> execute_script('config.py')
    ''
    """
    try:
        # Execute file_to_test and capture the output
        output = subprocess.check_output([sys.executable, file_to_test],
                                         text=True, timeout=30)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File '{file_to_test}' not found.") from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error executing '{file_to_test}'.") from e

    return output.strip()


def execute_test(test_script: str, file_to_test: str, challenge_id: str) -> str:
    """if a challenge provided its own test_solution.py tests, call it

    Args:
        test_script: the challenge/.../test_solution.py or generic_test.py
        file_to_test: the path to the user submitted code to test
        challenge_id: the str of the challenge number

    Returns:
        the output and/or error of the execution result

    Note: as long as the test script runs, its error messages will be included
    in the output. Only when the script could not run would it raise error.
    """
    try:
        # Execute pytest file_to_test and capture the output
        pytest_cmd = ["pytest", test_script, "-vv", "-rN", "--tb=short",
                      "--user_file", file_to_test, "--challenge_id", challenge_id]
        output = subprocess.run(pytest_cmd, text=True, timeout=30,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                shell=False, check=False)
        result = re.sub(r'.*(?:\n=+ FAILURES =+)',
                        '', output.stdout, flags=re.DOTALL)
        result = re.sub(r'(_+) (.*?) (_+)',
                        lambda m: m.group(1) + " " +
                        m.group(2).replace(r"\n", "\n")
                        .replace("[", "[\n").replace("]", "\n]") +
                        " " + m.group(3),
                        result)
        if output.stderr:
            result += ";" + output.stderr
        if output.returncode != 0:
            result = (f"TEST FAILED (rc={output.returncode}):{result}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File '{file_to_test}' not found.") from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Execution of '{file_to_test}' returned error."
                           ) from e
    except Exception as e:
        raise RuntimeError(f"Executing '{file_to_test}' failed.") from e

    return result


def check_submission(challenge_id: str, file_to_test: str) -> str:
    """Tests if user submission would produce expected output.

    First check if the challenge id has a test_solution.py file, if exist
    it means the challenge has it's own testing code, will delegate testing
    to this code; if does not exist, will use the "expected_output" in
    the problem.json as the target for assertion (usually this means the 
    problem is for non-function scripts).

    Args:
        challenge_id: the str of the challenge number
        file_to_test: the path to the script to execute

    Returns:
        the output and/or error of the execution result.

    >>> check_submission('1', 'user_submissions/test_user/1.py')
    'Test passed.'
    """
    challenge_test_file = os.path.join(config.CHALLENGE_DIR, challenge_id,
                                       config.TEST_FILENAME)
    test_module_file = challenge_test_file if os.path.exists(
        challenge_test_file) else "utils/generic_test.py"
    if os.path.exists(test_module_file):
        # test_solutions.py exist, will outsource checking to it
        exec_result = "did not execute"
        try:
            exec_result = execute_test(
                test_module_file, file_to_test, challenge_id)
            assert "Error" not in exec_result
            assert "failed" not in exec_result.lower()
        except Exception as e:
            raise ValueError(exec_result.strip()) from e
        else:
            return "Test passed."

    else:
        # fallback of executing the script directly and compare to expected
        with open(f"{config.CHALLENGE_DIR}/{challenge_id}/problem.json",
                  encoding='utf-8') as f:
            challenge_data = json.load(f)
            expected_output = challenge_data.get('expected_output')
            exec_result = "did not execute"
            try:
                exec_result = execute_script(file_to_test)
                assert exec_result == expected_output
            except Exception as e:
                raise ValueError(f"TEST FAILED:\n"
                                 f"expected: {expected_output.strip()},"
                                 f"got: {exec_result}") from e
            else:
                return "Test passed."


if __name__ == '__main__':
    import doctest
    doctest.testmod()
