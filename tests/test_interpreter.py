import unittest

from interpreter import formula_resolver


class TestInterpreter(unittest.TestCase):
    MATH_EXPRESSION_LIST = [
        ("3", 3),
        ("2 + 7 * 4", 30),
        ("7 - 8 / 4", 5),
        ("14 + 2 * 3 - 6 / 2", 17),
        ("7 + 3 * (10 / 2)", 22),
        ("7 + 3 * (10 / (3 - 1))", 22),
        ("7 + 3 * (10 / (12 / 4 - 1))", 22),
        ("7 + 3 * (10 / (12 / (3 + 1) - 1))", 22),
        ("7 + (((3 + 2)))", 12),
        ("- 3", -3),
        ("+ 3", 3),
        ("5 - - 3", 8),
        ("5 - - (3 + 4) - + 2", 10),
        ("3.14", 3.14),
        ("2.14 + 7 * 4", 30.14),
        ("7.14 - 8 / 4", 5.14),
        ("7 + 3 * 5 / 5 - 5 - 3 + (8)", 10),
        ("7 + 3 * (10 / (12 / 4 - 1)) / (5) - 5 - 3 + (8)", 10),
        ("7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)", 10),
        ("2 + 7 * 4", 30),
        ("3", 3),
        ("7 + (((3 + 2)))", 12),
        ("7 + 3 * (10 / (12 / (3 + 1) - 1))", 22),
        ("7 - 8 / 4", 5),
        ("14 + 2 * 3 - 6 / 2", 17),
        ("7 - 8 / 4", 5),
        ("1 * 2 + 3", 5),
        ("3 + 2 * 1", 5),
        ("4 + 3 * 1 ^ 2", 7),
        # ("1 ^ 2 * 3 + 4", 7),
    ]

    def test_generic_math_expression(self):
        for expr, expected in self.MATH_EXPRESSION_LIST:
            result = formula_resolver(expr)

            assert result == expected, (expr, result)


if __name__ == "__main__":
    unittest.main()
