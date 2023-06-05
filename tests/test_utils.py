import unittest

from lexer import lexer
from utils import parse_function_args, parse_parenthesis_expr


class TestUtils(unittest.TestCase):
    def test_parse_parenthesis_expr(self):
        expr = "(1)"
        tokens = iter(lexer(expr))
        parenthesis_expr = list(parse_parenthesis_expr(tokens))
        assert len(parenthesis_expr) == 1, parenthesis_expr
        assert len(list(tokens)) == 0

        expr = "(1 + (2 + 3)) + 4 + 5"
        tokens = iter(lexer(expr))
        parenthesis_expr = list(parse_parenthesis_expr(tokens))
        assert len(parenthesis_expr) == 7, parenthesis_expr
        assert len(list(tokens)) == 4

        expr = "((((1) + 2) + 3) + 4) + 5"
        tokens = iter(lexer(expr))
        parenthesis_expr = list(parse_parenthesis_expr(tokens))
        assert len(parenthesis_expr) == 13
        assert len(list(tokens)) == 2

        expr = "(1 + 2) + (3 + 4 + 5)"
        tokens = iter(lexer(expr))
        parenthesis_expr = list(parse_parenthesis_expr(tokens))
        assert len(parenthesis_expr) == 3
        assert parenthesis_expr[1].value == "+"
        assert len(list(tokens)) == 8

    def test_parse_parenthesis_expr_syntax_error(self):
        helper = lambda x: list(parse_parenthesis_expr(x))

        for expr in (")(", ")", "(", "((", "))"):
            tokens = iter(lexer(expr))
            self.assertRaises(SyntaxError, helper, tokens)

        expr = "((1 + 2) + (3 + 4) + 5"
        tokens = iter(lexer(expr))
        self.assertRaises(SyntaxError, helper, tokens)

        expr = "(1 + 2"
        tokens = iter(lexer(expr))
        self.assertRaises(SyntaxError, helper, tokens)

    def test_parse_function_args(self):
        expr = "(1, 2)"
        tokens = iter(lexer(expr))
        args = parse_function_args(tokens)
        assert len(args) == 2
        assert tuple(len(arg) for arg in args) == (1, 1)

        expr = "(1, (2 + 3))"
        tokens = iter(lexer(expr))
        args = parse_function_args(tokens)
        assert len(args) == 2
        assert tuple(len(arg) for arg in args) == (1, 5)

        expr = "(1, IF(2 < 3, 4, 5))"
        tokens = iter(lexer(expr))
        args = parse_function_args(tokens)
        assert len(args) == 2
        assert tuple(len(arg) for arg in args) == (1, 10)

        expr = "(1 + (2 + 3), 4 + 5, IF(A11, A12, A13))"
        tokens = iter(lexer(expr))
        args = parse_function_args(tokens)
        assert len(args) == 3
        assert tuple(len(arg) for arg in args) == (7, 3, 8)


if __name__ == "__main__":
    unittest.main()
