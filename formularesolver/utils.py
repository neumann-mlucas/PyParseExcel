from typing import Iterator

from lexer import LParenthesis, Token, get_precedence


def needs_swap(left_token: Token, right_token: Token) -> bool:
    "evaluates if the right token has higher precedence than the left token -- aka if a node swap is needed"
    assert left_token.type == "operator"
    if right_token.type in ("operator", "function", "symbol"):
        return get_precedence(left_token) > get_precedence(right_token)
    return False


def parse_parenthesis_expr(tokens: Iterator[Token]) -> Iterator[Token]:
    "returns all tokens inside the top level parenthesis"
    depth = 0
    for token in tokens:
        match (token.value, depth):
            case _ if depth < 0:
                raise SyntaxError("Unmatched Parenthesis")
            case (")", 1):
                return
            case (")", _):
                depth -= 1
            case ("(", 0):
                depth += 1
                continue
            case ("(", _):
                depth += 1
        yield token
    raise SyntaxError("Unmatched Parenthesis")


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
        buf.append(token)
    yield buf


def parse_function_args(tokens: Iterator[Token]) -> list[list[Token]]:
    "parse tokens inside function parenthesis e.g. fn( ... )"
    args = parse_parenthesis_expr(tokens)
    args = split_args(args)
    return list(args)  # need to consume iterator here
