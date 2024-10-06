"""generating test cases of problem:solution pairs

This should only be used for generating test_cases for non-function scripts.
For all function based .py code, they should use their own test_solution.py

Usage:
    pythong -m challenge.id.gen_pj.py
"""

from utils.generate_problem_json import generate_problem_json, print_result


problem: dict = {
    "title": "bitwise operations",
    "goal": "understanding the bitwise NOT, AND, XOR, OR and shift",
    "description": """
""",
    "notes": "when answering a type question use quotation marks i.e. 'int'; "
    "it is expected that running this program does not produce any output.",
    "condition_code": """\
a = 0b10011010
b = 0b00110111
c = 13
d = 105
""",
    "starting_code": """\
# given the below values of variable a to d, complete the following code: 

# print the value of a and bitwise NOT a:
print(,)

# manually calculate bitwise NOT of b, and NOT c, and add answer to the 
#  right side of = of the following assignment statement 
# (hint, for b, you can flip each bit, but 0b format are unsigned, you will 
#  need to manually convert the result as a signed integer, since it has 8 bits,
#  the highest bit is used as sign, so you need to subtract the result by 256, 
#  this is needed because integers are signed internally, but 0b format is 
#  unsigned ;
#  for c, you actually don't need to do it bit by bit, although it is 
#  perfectly legit to convert it to binary and do it as b.):
answer_bitwise_not_b = 
answer_bitwise_not_c = 
print(answer_bitwise_not_b, answer_bitwise_not_c)

# consider a and c, with bitwise AND, XOR, OR, which operation of these
#  two values will produce the largest amount, what is the result value of this
#  operation? (use an expression to answer, but you need to know which
#  operation produce the largest result):
answer_largest_bitwise_operation_of_a_and_c = 
print(answer_largest_bitwise_operation_of_a_and_c)

# The following code tries to multiply d by c using bitwise operations.
# To simplify the solution, we will use add operation +, but we have
# shown using bitwise operation to realize addition, so it's possible to
# completely realize multiplication using bitwise operations only.
# Your task is to complete the missing parts of the code below (note, we 
# intentionally break down the steps to step_0 to step_4, so we can check the
# intermediate results and make sure you did everything correctly.  With 4 
# steps, we will only be able to handle c<=15, that is ok for now.)

# step0
multiplier = c
result = 0
multiplicand = d

# step1
print(result)
if multiplier & 1: 
    result += multiplicand
multiplicand = multiplicand << 1

# step2
print(result)
if multiplier & 2:
    result += multiplicand
multiplicand <<= 1

# based on the above lines, use same logic, please finish ...step_3 
# and ...ste_4, so that final result equals d * c
# (please print intermediate result like above.)


# final result
print(result)
""",
    "expected_output": ""
}
starting_condition = ["""\
a = 24
b = 83
c = 11
d = 72
"""]


def solution() -> str:
    """the actual solution that will generate the expected output"""
    from utils.generate_problem_json import print

    print(a, ~a)
    print(0b11001000 - 256, -13 - 1)
    print(a | c)
    cc = c
    dd = d
    result = 0
    for i in range(4):
        print(result)
        if cc & 2 ** i:
            result += dd
        dd <<= 1
    print(result)
    return print_result()


if __name__ == '__main__':
    generate_problem_json(__file__, problem, starting_condition, solution,
                          globals())
