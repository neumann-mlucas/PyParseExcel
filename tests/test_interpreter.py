import unittest

from interpreter import formula_resolver

TEST_VARIABLES = {
    "A1": 1,
    "A2": 1,
    "A3": 1,
    "A4": 1,
    "A5": 1,
    "A6": 1,
    "A7": 1,
    "A8": 1,
    "A9": 1,
    "A10": 1,
    "B1": 2,
    "B2": 2,
    "B3": 2,
    "B4": 2,
    "B5": 2,
    "B6": 2,
    "B7": 2,
    "B8": 2,
    "B9": 2,
    "B10": 2,
}


class TestInterpreter(unittest.TestCase):
    MATH_EXPRESSIONS = [
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
        ("1 ^ 2 * 3 + 4", 7),
        ("(1)", 1),
        ("((((1) + 2) + 3) + 4) + 5", 15),
        ("10 * 20%", 2),
    ]

    LOGICAL_OPERATORS = [
        ("1 = 1", True),
        ("1 = 2", False),
        ("1 <> 2", True),
        ("1 <> 1", False),
        ("1 <= 1", True),
        ("1 <= 2", True),
        ("2 <= 1", False),
        ("1 >= 1", True),
        ("1 >= 2", False),
        ("2 >= 1", True),
        ("2 > 1", True),
        ("1 > 2", False),
        ("1 < 2", True),
        ("2 < 1", False),
    ]

    FUNCTION_EXPR = [
        ('IF(FALSE, "foo", "bar")', "bar"),
        ('IF(TRUE, "foo", "bar")', "foo"),
        ('IF(NOT(FALSE), "foo", "bar")', "foo"),
        ('IF(1 > 2, "foo", "bar")', "bar"),
        ('IF(1 < 2, "foo", "bar")', "foo"),
        ("MAX(1,2,3,4,5)", 5),
        ("AND(2 > 1, 2 < 3)", True),
        ("OR(2 < 1, 2 < 3)", True),
    ]

    MISC_EXPR = [
        ('"foo" & "bar"', "foobar"),
    ]
    RANGE_EXPR = [
        ("SUM(A1:A5)", 5),
        ("SUM(A1:A10)", 10),
        ("SUM(B6:B10)", 10),
        ("SUM(B1:B10)", 20),
        ("SUM(A1:B5)", 15),
        ("SUM(A1:B10)", 30),
    ]

    def test_generic_math_expression(self):
        for expr, expected in self.MATH_EXPRESSIONS:
            result = formula_resolver(expr)
            assert result == expected, (expr, result)

    def test_logical_operator_expression(self):
        for expr, expected in self.LOGICAL_OPERATORS:
            result = formula_resolver(expr)
            assert result == expected, (expr, result)

    def test_functions(self):
        for expr, expected in self.FUNCTION_EXPR:
            result = formula_resolver(expr)
            assert result == expected, (expr, result)

    def test_range_functions(self):
        for expr, expected in self.RANGE_EXPR:
            result = formula_resolver(expr, TEST_VARIABLES)
            assert result == expected, (expr, result)


if __name__ == "__main__":
    unittest.main()
