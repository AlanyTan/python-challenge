"""individual challenge test user submission"""


def test_solution(user_file: str, capsys) -> None:
    """run the user submitted code to test it.

    Usage:
        pytest test_solution -qq -rN -tb=short --user_file=submissions/u1/1.py
    """
    with open(user_file, "rt", encoding='utf-8') as uf:
        code_submitted = uf.read()

    exec(code_submitted)
    l = locals()
    assert l['a'] == 42
    assert l['b'] == 3.14
    assert l['b'] is l['c']
    assert l['d'] == "words"
    assert l['e'] == b"bytes"
    assert l['f'] is True
    assert l['g'] is l['f']
    assert l['h'] is None
    assert l['a'] is l['i']
    assert l['b'] is l['j']
    assert l['k'] == l['a'] + l['j']
