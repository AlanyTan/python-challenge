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
    assert l['a'] == 1
    assert l['b'] == 0.0
    assert l['c'] == '0'
    assert l['d'] == ""
    assert l['e'] is True
    assert l['f'] == 'False'
    assert l['g'] is None
    assert l['answer_is_a_bool_type'] is False
    assert l['answer_is_not_a_bool_type'] is True
    assert l['answer_is_b_Truthy'] is False
    assert l['answer_is_c_Truthy'] is True
    assert l['answer_is_d_Truthy'] is False
    assert l['answer_is_e_Truthy'] is True
    assert l['answer_is_f_Truthy'] is True
    assert l['answer_is_g_Truthy'] is False
    assert l['answer_a_and_b_is_of_type'] in str(type(l['a'] and l['b']))
    assert l['answer_b_or_c_is_of_type'] in str(type(l['b'] or l['c']))
    assert l['answer_not_d_or_2e_is_of_type'] in str(type(not l['d'] or
                                                          l['e'] * 2))
    assert l['answer_b_or_not_d_and_2e_is_of_type'] in str(type(l['b'] or
                                                                not l['d'] and
                                                                l['e'] * 2))
    assert l['e'] is True
    assert l['e'] is True
    assert l['e'] is True
    assert l['e'] is True
    assert l['e'] is True
