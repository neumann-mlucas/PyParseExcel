from itertools import chain
from typing import Iterator, Self

from lexer import Token
from utils import needs_swap, parse_function_args, parse_parenthesis_expr


class ASTNode:
    "Abstract Syntax Tree Node"

    def __init__(self, token: Token, children: list[Self] | None = None):
        self.token = token
        self.children = children if children is not None else []

    def __iter__(self) -> list[Self]:
        return self.children

    def __getitem__(self, key: int) -> Self:
        return self.children[key]

    def __len__(self) -> int:
        return len(self.children)

    def __repr__(self) -> str:
        return self.pprint()

    def pprint(self, depth: int = 0) -> str:
        tabs = "\t" * depth
        children = "".join(
            sorted(node.pprint(depth=depth + 1) for node in self.children)
        )
        return (
            f"{tabs}<NODE:{self.token.type.upper()} [{self.token.value}] >\n{children}"
        )

    @property
    def is_end_node(self) -> bool:
        return all(node.childless for node in self.children)

    @property
    def childless(self) -> bool:
        return self.children == []

    def walk(self) -> Iterator[Token]:
        yield self.token
        for node in self.children:
            yield from node.walk()


class VariableNode(ASTNode):
    pass


class ConstantNode(ASTNode):
    pass


class FunctionNode(ASTNode):
    pass


class ParenthesesNode(ASTNode):
    pass


def parser(tokens: Iterator[Token], parent=None) -> ASTNode:
    "consume a list of token to assemble a AST"

    # clean up some call of iter() from the code
    if isinstance(tokens, list):
        tokens = iter(tokens)

    try:
        token = next(tokens)
    except StopIteration:
        return parent  # base case

    match token:
        case Token("variable"):
            node = ASTNode(token)
            return parser(tokens, node)

        case Token("constant"):
            node = ConstantNode(token)
            return parser(tokens, node)

        case Token("function"):
            args = parse_function_args(tokens)
            args = [parser(iter(arg)) for arg in args]
            node = FunctionNode(token, args)
            return parser(tokens, node)

        case Token("operator"):
            left_operand = parent
            right_operand = parser(tokens)

            # invert nodes if right priority > left priority
            if needs_swap(token, right_operand.token):
                parent = right_operand
                node = FunctionNode(
                    token, [left_operand, right_operand.children.pop(0)]
                )
                right_operand.children.append(node)
                return right_operand

            node = FunctionNode(token, [left_operand, right_operand])
            return parser(tokens, node)

        case Token("symbol", "("):
            expr = parse_parenthesis_expr(chain([token], tokens))
            node = ParenthesesNode(token, [parser(iter(expr), parent)])
            return parser(tokens, node)

        case _:
            raise SyntaxError(f"Invalid token: {token}")
