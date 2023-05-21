from typing import Iterator

from lexer import Token, get_precedence
from utils import parse_function_args, parse_parenthesis_expr


def needs_swap(left_token: Token, right_token: Token) -> bool:
    "evaluates if the right token has higher precedence than the left token -- aka if a node swap is needed"
    if right_token.type == "operator" or right_token.value == "/":
        return get_precedence(left_token) > get_precedence(right_token)
    return False


class ASTNode:
    "Abstract Syntax Tree Node"

    def __init__(self, token: Token, children: list | None = None):
        self.type = token.type
        self.value = token.value
        self.token = token
        self.children = children if children is not None else []

    def __iter__(self) -> list["ASTNode"]:
        return self.children

    def __getitem__(self, key) -> "ASTNode":
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
        return f"{tabs}<NODE:{self.type.upper()} [{self.value}] >\n{children}"

    @property
    def is_end_node(self) -> bool:
        return all(node.childless for node in self.children)

    @property
    def childless(self) -> bool:
        return self.children == []

    def walk(self):
        yield self.token
        for node in self.children:
            yield from node.walk()


def parser(tokens: Iterator[Token], parent=None) -> ASTNode:
    "consume a list of token to assemble a AST"

    # clean up some call of iter from the code
    if isinstance(tokens, list):
        tokens = iter(tokens)

    try:
        token = next(tokens)
    except StopIteration:
        return parent

    match token:
        case ("variable", _) | ("constant", _) | ("boolean", _):
            node = ASTNode(token, None)
            return parser(tokens, node)

        case ("function", _):
            args = parse_function_args(tokens)
            args = [parser(iter(arg)) for arg in args]
            node = ASTNode(token, args)
            return parser(tokens, node)

        case ("operator", _):
            left_operand = parent
            right_operand = parser(tokens)

            # invert nodes if right priority > left priority
            if needs_swap(token, right_operand.token):
                parent = right_operand
                node = ASTNode(token, [left_operand, right_operand.children.pop(0)])
                right_operand.children.append(node)
                return right_operand

            node = ASTNode(token, [left_operand, right_operand])
            return parser(tokens, node)

        case ("symbol", "("):
            expr = parse_parenthesis_expr(tokens)
            node = ASTNode(token, [parser(iter(expr), parent)])
            return parser(tokens, node)

        case _:
            raise SyntaxError(f"Invalid token: {token}")
