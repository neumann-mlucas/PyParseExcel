import unittest

from lexer import lexer
from utils import parse_function_args, parse_parenthesis_expr


class TestUtils(unittest.TestCase):
    def test_parse_parenthesis_expr(self):
        tokens = iter(lexer("(1 + (2 + 3)) + 4 + 5"))
        next(tokens)  # parser consumes first LParenthesis
        parenthesis_expr = list(parse_parenthesis_expr(tokens))
        assert len(parenthesis_expr) == 7
        assert len(list(tokens)) == 4

    def test_parse_function_args(self):
        tokens = iter(lexer("(1 + (2 + 3), 4 + 5, IF(A11, A12))"))
        args = parse_function_args(tokens)
        assert len(args) == 3
        assert tuple(len(arg) for arg in args) == (7, 3, 6)


if __name__ == "__main__":
    unittest.main()
