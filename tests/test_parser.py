import unittest
from parser import parser

from lexer import lexer


class TestParser(unittest.TestCase):
    def test_operator_precedence(self):
        expr = "1 * 2 + 3"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.token.value == "+"
        assert ast[1].token.value == "*"

        expr = "1 * (2 + 3)"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.token.value == "*"
        assert ast[1][0].token.value == "+"

        expr = "1 * (2 + 3) + 4"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.token.value == "+"
        assert ast[0].token.value == 4

        expr = "1 ^ 2 * 3 + 4"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.token.value == "+"
        assert ast[0].token.value == "*"

        expr = "1 : 2 & 3 + 4"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.token.value == "&"
        assert ast[0].token.value == "+"
        assert ast[1].token.value == ":"

    def test_function_parameter(self):
        expr = "1 + IF(A1, A2, A3)"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast[1].token.value == "IF"
        assert len(ast[1].children) == 3

        expr = '1 + IF(A1 * (B2 + C3) , ABS(D4), IF(E5, "YES", "NO"))'
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast[1].token.value == "IF"
        assert len(ast[1].children) == 3

    def test_parenthesis_expr(self):
        expr = "(1)"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.token.value == "("
        assert ast[0].token.value == 1

        expr = "((((1) + 2) + 3) + 4) + 5"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast[1].token.value == 5, ast[0].value

        expr = "(1 + 2) + (3 + 4 + 5)"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.token.value == "+"

        expr = ")("
        tokens = iter(lexer(expr))
        self.assertRaises(SyntaxError, parser, tokens)

        expr = "((1 + 2) + (3 + 4) + 5"
        tokens = iter(lexer(expr))
        self.assertRaises(SyntaxError, parser, tokens)

        expr = "(1 + 2"
        tokens = iter(lexer(expr))
        self.assertRaises(SyntaxError, parser, tokens)

    def test_unary_operators(self):
        expr = "-1"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.token.value == "-"
        assert ast[0].token.value == 1


if __name__ == "__main__":
    unittest.main()
