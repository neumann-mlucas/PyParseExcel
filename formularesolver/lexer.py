import re
from collections import namedtuple


class SyntaxError(Exception):
    pass


Token = namedtuple("Token", ["name", "value"])
LParenthesis = Token("symbol", "(")
RParenthesis = Token("symbol", ")")
Comma = Token("symbol", ",")
EOL = Token("symbol", "EOL")

RE_VAR = re.compile(r"[A-Z]+[1-9]+").match
RE_STR = re.compile(r"\".*\"$").match
RE_INT = re.compile(r"[0-9]+$").match
RE_FLOAT = re.compile(r"[0-9]+[.,]{1}[0-9]+$").match


def lexer(chars: str) -> list[Token]:
    "converts raw expression in a list of tokens"
    clean_chars = chars.replace(",", " , ").replace("(", " ( ").replace(")", " ) ")
    return [lexer_mapper(char) for char in clean_chars.split()]


def lexer_mapper(char: str) -> Token:
    "maps a word from the raw expression to a token"
    match char:
        case "TRUE" | "FALSE":
            return Token("boolean", char)
        case "SUM" | "MEAN" | "IF" | "AND" | "ABS":
            return Token("function", char)
        case "*" | "/" | "+" | "-":
            return Token("operator", char)
        case "(" | ")" | ",":
            return Token("symbol", char)
        case _:
            pass

    if RE_FLOAT(char):
        return Token("constant", float(char))
    elif RE_INT(char):
        return Token("constant", int(char))
    elif RE_STR(char):
        return Token("constant", char)
    elif RE_VAR(char):
        return Token("variable", char)
    else:
        raise SyntaxError(f"Unknown symbol: {char}")


def priority(token: Token) -> int:
    "returns the priority list of a token"
    match (token.name, token.value):
        case ("symbol", "("):
            return 4
        case ("function", _):
            return 3
        case ("operator", "*"):
            return 2
        case ("operator", "/"):
            return 2
        case ("operator", "+"):
            return 1
        case ("operator", "-"):
            return 1
        case _:
            return 0
