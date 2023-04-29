from itertools import takewhile
from typing import Iterator

from lexer import Comma, LParenthesis, RParenthesis, Token


def split_at(pred, iterable, max_split=-1, keep_separator=False):
    if max_split == 0:
        yield list(iterable)
        return

    buf = []
    it = iter(iterable)
    for item in it:
        if pred(item):
            yield buf
            if keep_separator:
                yield [item]
            if max_split == 1:
                yield list(it)
                return
            buf = []
            max_split -= 1
        else:
            buf.append(item)
    yield buf


def parse_function_args(tokens: Iterator[Token]) -> list[list[Token]]:
    "parse tokens inside function parenthesis e.g fn( ... )"
    lp = next(tokens)  # LParenthesis
    assert lp == LParenthesis, lp

    args = takewhile(lambda t: t != RParenthesis, tokens)
    args = split_at(lambda t: t == Comma, args)
    args = list(args)  # need to consume iterator here

    return args


def parse_parenthesis_expr(tokens: Iterator[Token]) -> list[Token]:
    "parse tokens inside parenthesis e.g ( expr )"
    args = takewhile(lambda t: t != RParenthesis, tokens)
    return list(args)
