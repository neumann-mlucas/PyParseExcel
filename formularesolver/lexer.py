import re
from collections import namedtuple
from typing import Iterator


class SyntaxError(Exception):
    pass


FUNCTIONS_LOGICAL = (
    "AND",
    "IF",
    "NOT",
    "OR",
    "XOR",
)
FUNCTIONS_MATH = (
    "ABS",
    "CEIL",
    "COS",
    "EXP",
    "FLOOR",
    "LOG",
    "LOG10",
    "MAX",
    "MIN",
    "PI",
    "ROUND",
    "SIN",
    "SUM",
    "TAN",
)
OPERATORS = (
    r"\&",
    r"\:",
    r"\-",
    r"\+",
    r"\*",
    r"\/",
    r"\%",
    r"\^",
)
LOGICAL_OPERATORS = (
    r"\=",
    r"\<\>",
    r"\<\=",
    r"\>\=",
    r"\<",
    r"\>",
)
SYMBOLS = (
    r"\(",
    r"\)",
    r"\,",
)


# VARIABLES
RE_CELL_REF = re.compile(r"\$?[A-Z]+\$?[0-9]+").match
# DATE TYPES
RE_BOOL = re.compile("TRUE|FALSE").match
RE_STRING = re.compile(r"\".*?\"").match
RE_INT = re.compile(r"[0-9]+").match
RE_FLOAT = re.compile(r"[0-9]+\.[0-9]+").match
RE_FLOAT_SCIENTIFIC = re.compile(r"[0-9]+(e|E)[\+\-]?[0-9]+").match

# SPECIAL CHARACTERS
RE_SYMBOLS = re.compile(r"|".join(SYMBOLS)).match
RE_SPACE = re.compile(r"\s+").match

# FUNCTIONS AND OPERATORS
RE_OPERATOR = re.compile(r"|".join(LOGICAL_OPERATORS + OPERATORS)).match
RE_FUNCTION = re.compile(r"|".join(FUNCTIONS_MATH + FUNCTIONS_LOGICAL)).match

Token = namedtuple("Token", ["type", "value"])
LParenthesis = Token("symbol", "(")
RParenthesis = Token("symbol", ")")
Comma = Token("symbol", ",")


def lexer(expression: str) -> Iterator[Token]:
    "converts a raw expression in a list of tokens"
    # base case
    if expression == "":
        return
    # Ignore Space
    elif m := RE_SPACE(expression):
        pass
    # Symbols, Operator and Functions
    elif m := RE_SYMBOLS(expression):
        yield Token("symbol", m.group())
    elif m := RE_OPERATOR(expression):
        yield Token("operator", m.group())
    elif m := RE_FUNCTION(expression):
        yield Token("function", m.group())
    # Excel Variables
    elif m := RE_CELL_REF(expression):
        yield Token("variable", m.group())
    # Excel Data Types
    elif m := RE_BOOL(expression):
        yield Token("constant", m.group() == "TRUE")
    elif m := RE_STRING(expression):
        yield Token("constant", m.group().replace('"', ""))
    elif m := RE_FLOAT(expression):
        yield Token("constant", float(m.group()))
    elif m := RE_FLOAT_SCIENTIFIC(expression):
        yield Token("constant", float(m.group()))
    elif m := RE_INT(expression):
        yield Token("constant", int(m.group()))
    # Unknown Token
    else:
        raise SyntaxError(f"Invalid Token in Expression: {expression}")

    expression = expression.removeprefix(m.group())
    yield from lexer(expression)


def get_precedence(token: Token) -> int:
    "returns the precedence of a given token"
    match token:
        case ("symbol", "("):
            return 1000
        case ("function", _):
            return 990
        case ("operator", ":"):
            return 980
        case ("operator", "unary -" | "unary +"):
            return 971
        case ("operator", "%"):
            return 970
        case ("operator", "^"):
            return 960
        case ("operator", "*" | "/"):
            return 950
        case ("operator", "+" | "-"):
            return 940
        case ("operator", "&"):
            return 930
        case ("operator", _):
            return 920  # comparison operators
        case _:
            return 0
