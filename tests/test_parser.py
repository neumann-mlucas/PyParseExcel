import unittest
from parser import FunctionNode, parser

from lexer import lexer


class TestParser(unittest.TestCase):
    def test_operator_precedence(self):
        expr = "1 * 2 + 3"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "+"
        assert ast[0].value == "*"

        expr = "1 * (2 + 3)"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "*"
        assert ast[1][0].value == "+"

        expr = "1 * (2 + 3) + 4"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "+"
        assert ast[1].value == 4

    def test_multi_operator_precedence(self):
        expr = "1 : 2 & 3 + 4"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "&"
        assert ast[0].value == ":"
        assert ast[1].value == "+"

        expr = "4 + 3 * 1 ^ 2"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "+"
        assert ast[1].value == "*"

        expr = "1 ^ 2 * 3 + 4"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "+"
        assert ast[0].value == "*"

    def test_function_parameter(self):
        expr = "1 + IF(A1, A2, A3)"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast[1].value == "IF"
        assert len(ast[1].children) == 3

        expr = '1 + IF(A1 * (B2 + C3) , ABS(D4), IF(E5, "YES", "NO"))'
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast[1].value == "IF"
        assert len(ast[1].children) == 3

    def test_parenthesis_expr(self):
        expr = "(1)"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "("
        assert ast[0].value == 1

        expr = "((((1) + 2) + 3) + 4) + 5"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast[1].value == 5, ast[0].value

        expr = "(1 + 2) + (3 + 4 + 5)"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "+"

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
        assert ast.value == "unary -"
        assert ast[0].value == 1

        expr = "1 + + 2"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "+"
        assert ast[1].value == "unary +"

        expr = "1 - - 2"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "+"
        assert ast[0].value == 1
        assert ast[1].value == "unary -"

        expr = "- 2 + 3"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "+"
        assert ast[0].value == "unary -"

        expr = "- 2 + - 3"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "+"
        assert ast[0].value == "unary -"
        assert ast[1].value == "unary -"

        expr = "- (1 + 2)"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "unary -"

    def test_operators_errors(self):
        expr = "1 * * 2"
        tokens = iter(lexer(expr))
        self.assertRaises(SyntaxError, parser, tokens)

        expr = "1 -"
        tokens = iter(lexer(expr))
        self.assertRaises(SyntaxError, parser, tokens)

    def test_percent_operator(self):
        expr = "10%"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert isinstance(ast, FunctionNode)

        expr = "%10"
        tokens = iter(lexer(expr))
        self.assertRaises(SyntaxError, parser, tokens)

        expr = "20% * 10"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "*"
        assert ast[0].value == "%"

        expr = "10 * 20%"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "*"
        assert ast[1].value == "%"

        expr = "-20%"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "%"
        assert ast[0].value == "unary -"

        expr = "1:20%"
        tokens = iter(lexer(expr))
        ast = parser(tokens)
        assert ast.value == "%"
        assert ast[0].value == ":"


if __name__ == "__main__":
    unittest.main()
