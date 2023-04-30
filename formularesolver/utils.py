from typing import Iterator

from lexer import LParenthesis, Token


def parse_parenthesis_expr(tokens: Iterator[Token]) -> Iterator[Token]:
    "returns all tokens inside the top level parenthesis"
    depth = 0
    for token in tokens:
        match (token.value, depth):
            case (")", 0):
                break
            case (")", _):
                depth -= 1
            case ("(", _):
                depth += 1
            case (_, -1):
                raise SyntaxError("unmatched parenthesis")
        yield token


def split_args(tokens: Iterator[Token]) -> Iterator[list[Token]]:
    "split a expression on top level commas"
    depth, buf = 0, []
    for token in tokens:
        match (token.value, depth):
            case (",", 0):
                yield buf
                buf = []
                continue
            case ("(", _):
                depth += 1
            case (")", _):
                depth -= 1
            case (_, -1):
                raise SyntaxError("unmatched parenthesis")
        buf.append(token)
    yield buf


def parse_function_args(tokens: Iterator[Token]) -> list[list[Token]]:
    "parse tokens inside function parenthesis e.g. fn( ... )"
    lp = next(tokens)
    assert lp == LParenthesis, lp

    args = parse_parenthesis_expr(tokens)
    args = split_args(args)
    return list(args)  # need to consume iterator here
