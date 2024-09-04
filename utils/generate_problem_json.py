"""utility tools used by code to generate problem.json"""

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


if __name__ == '__main__':
    print(1, "str", False)
    original_print(print_result())
