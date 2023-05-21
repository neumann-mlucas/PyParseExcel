import unittest

from lexer import Token, lexer

ONE = Token("constant", 1)
SUM = Token("function", "SUM")
PLUS = Token("operator", "+")
COMMA = Token("symbol", ",")
RPARENTHESIS = Token("symbol", "(")
LPARENTHESIS = Token("symbol", ")")
FOO = Token("constant", "foo")
BAR = Token("constant", "bar")


class TestLexer(unittest.TestCase):
    def test_mix_spacing(self):
        expected = [ONE, PLUS, ONE]
        assert expected == list(lexer("  1  +   1 "))
        assert expected == list(lexer("1+1"))

        expected = [SUM, RPARENTHESIS, ONE, COMMA, ONE, LPARENTHESIS]
        assert expected == list(lexer("  SUM( 1,     1)  "))
        assert expected == list(lexer("SUM(1,1)"))

    def test_number_formats(self):
        assert [Token("constant", 1)] == list(lexer("1"))
        assert [Token("constant", 1)] == list(lexer("0001"))
        assert [Token("constant", 1.0)] == list(lexer("1.0"))
        assert [Token("constant", 1.0)] == list(lexer("1.000"))
        assert [Token("constant", 1.0)] == list(lexer("01.0"))
        assert [Token("constant", 10.0)] == list(lexer("1e1"))
        assert [Token("constant", 10.0)] == list(lexer("1e+1"))
        assert [Token("constant", 0.1)] == list(lexer("1e-1"))

    def test_excel_variables(self):
        assert "variable" == next(lexer("$AB$12")).type
        assert "variable" == next(lexer("AB$12")).type
        assert "variable" == next(lexer("$AB12")).type
        assert "variable" == next(lexer("AB12")).type
        assert "variable" != next(lexer('"AB12"')).type

    def test_string_parsing(self):
        assert [FOO, BAR] == list(lexer('"foo" "bar"'))
        assert [FOO, ONE, BAR, BAR] == list(lexer('"foo" 1 "bar" "bar"'))


if __name__ == "__main__":
    unittest.main()
