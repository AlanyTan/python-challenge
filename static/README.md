# A challenge - test solution platform
Allows user to code online using code editr and submit their solution to challenges to be
evaluated by the platform. 

## Challenges organized as follow
The challenges are managed as file system structure under ./challenges
each challenge has its own subdir. Main asset for the challenge is problem.json

the problem.json look like this: 
```
{
    "title": "arithmatic operations",
    "goal": "understand how to combine arithmatic operations",
    "description": "With a, b, c print the result of:\n the sum of a, b and c\n sum of a and b then multiplied by c\n raise the sum of a and b to the power of c then multiplied by a\n double a and print the result\n the euclidean-quotient of the sum of a and b divided by c\n the remainder of the division of a and sum of b and c.",
    "notes": "Each line of question above should be printed on its own line.",
    "starting_code": "# ***Do not change this part***\na = 3\nb = 5\nc = 4\n# ***End of Do-not-change part***\n",
    "expected_output": "12\n32\n12288\n6\n2\n6",
    "test_cases": [["a=2\nb=1\nc=3\n", "6\n9\n54\n4\n1\n0"],["a=-1\nb=0\nc=1\n", "0\n-1\n1\n-2\n-2\n0"],["a=10\nb=2\nc=4\n", "16\n48\n207360\n20\n5\n2"]]
}
```
### challenge intro
The "title", "goal", description", "notes" are shown to the user as intro, explaining what this challenge is about, and what they need to solve.
### starting code
The "starting_code" are inserted into the code editor automatically. 
The "expected_output" is what is expected from the execution of the code, irrespective if the starting_code has been changed. 

### test cases
The "test_cases" are additional test cases to try. It's a list of lists, the inner list is a two element pair where the first element means the testing condition, the second element is the expected output. 
It is optional, you can ommit it, or set it to an empty list [].
If provided, the user is expected to keep the starting_code intact (otherwise, the additional test cases won't be able to replace starting_code with the first element of each test case), because the test script will replace the starting_code with the first element of each test case, and expect the rest of the code to execute to produce outcome equal to the second element of each test case.

### multi tab code editor support with python syntax highlighter
The page support multi tab code editor, when you save a file (or import a file from the book's stock examples), the tab name is changed to the filename. 
you can switch between tabs, only the current tab is visible, and code in it can execute. Other tabs will retain their code, once you switch to them, you can execute. 


### Handling Files
You can save files both using python open(filename, "w"), and the "Save VMFile" button. 
Your Python code can only interact with the VM's file system, so you open/read/write are against the VM. 

## Dependencies
### CodeMirror
This is the code editer. It can be downloaded via https://github.com/codemirror/codemirror5 (use the get the ZIP file option to avoid downloading stuff from the internet during runtime)

### Pyodide
This is the Python run time. NOTE: pyodide needs a webserver, it does not work locally from file://
Download it from: https://github.com/pyodide/pyodide/releases, extract it to pyodide dir (the default)
