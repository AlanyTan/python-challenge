# Challenge directory

This is the directory for challenges (problems and solutions)

## dir structure
The challenges are grouped in dir structures, a dir containing problem.json is considered a challenge. Whether or not a dir has problem.json, it can have subdirs, which can be another challenge. 

The challenge can have an optiona test_solution.py file to test it. 
It is recommended for challenges that pass the function level courses to use functions for the expected solutions, and use test_solutions.py to test the solution functions.
However, before students learned function, one can use the problem.json's "expected_output" field to check if the students submitted a solution that produces the expected output. 

## the problem.json
The problem.json files should contain at least "title", "goal", "description", "notes". And it can also contain additional fields "starting_code", "condition_code" and "expected_output.
The mandatory fields are self explainatory, they are provided as instructions for the students of what this challenge is about, and what are expected outcome. 

The "condition_code" is special in that it will present a "#### do not change this section ##### block of code in the coding area, and provide initial conditions, i.e. initial value for certain variables; this section COULD be replaced by the starting condition of addtional test cases!!!  The students are expected to keep this section intact, otherwise, they may fail the evaluation (because the evaluation looks to replace this section with different conditions, so if the students change this section, the replace will fail, and additional test cases will also fail.)  Note: "condition_code" is optional, it can be ommitted which simply means no starting condition needs to be set.

The "starting_code" on the other hand, gives the student a starting point, like partial code, or comments that tell them what is expected at each section. The starding_code can (actually should) be changed by the students in their solution submission. 

The "expected_output" is what the solution should produce with the condition_code. If this is omitted, it simply means the code should not produce any output.

The "test_cases" is a list of lists, the inner list is a pair of pieces of info, the alternative starting condition_code, and the alternative expected_output. This allows the challenge builder to test the user's submission with different set of conditions, so that it makes sure the code works isntead of hardcoded the output. This is optional, if not provided, only "condition_code" and "expected_output" are checked.

All four of the optional fields can be omitted, which will basically mean an empty starting point that should produce no output, and it actually passes the evaluation. 

While it is possible to manually create this file by stating the challenge in the test fields, and filling the "expected_output", it is easier to use a gen_pj.py file below: 

### the gen_pj.py
#### the problem and starting_condition objects
a gen_pj.py file can be created in the challenge dir and executing it shall create the problem.json file for you, this will allow easier (i.e. line wrap) creation of the problem object and filling the expected_output and test cases. 
First, it should define a problem dict and you can use Python syntax (including line wraps) to edit the content for this dict. 

Next, you can define a list of starting_condition, which initial value should be an empty list []. 

Then you should add your solution code to the solution function.

#### the generate_problem_json function
The main flow should import generate_problem_json function from utils.generate_problem_json module, with 5 arguments: 
- fn: the filename of the calling script (this is used to determine where      shall we save the problem.json to)
- problem: the problem dict you created, it will be updated with results before written to the problem.json file
- starting_condition: this is the list of alternative starting codition_code
- solution, the function that you put your solution code in
- global_scope: use globals() function to give your global scope to the generate_problem_json function. 

This function will run your solution with condition_code, and add its output as "expected_output" to problem dict; then it will iterate through starting_condition and use its entries to replace the condition_code to execute it once, receive the output, and add this starting condition, output as a pair (a tuple) to the "test_cases" list of the problem dict
After executing solution() against all alternative starting_code, it writes the problem dict to problem.json in the same dir as the fn. 

