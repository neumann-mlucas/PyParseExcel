from itertools import chain
from typing import Iterator, Self

from lexer import Token
from utils import needs_swap, parse_function_args, parse_parenthesis_expr


class ASTNode:
    "Abstract Syntax Tree Node"

    def __init__(self, token: Token, children: list[Self] | None = None):
        self.token = token
        self.value = token.value
        self.children = children if children is not None else []

    def __iter__(self) -> list[Self]:
        return self.children

    def __getitem__(self, key: int) -> Self:
        return self.children[key]

    def __len__(self) -> int:
        return len(self.children)

    def __repr__(self) -> str:
        return self.pprint()

    def __bool__(self) -> bool:
        return True

    def pprint(self, depth: int = 0) -> str:
        tabs = "\t" * depth
        children = "".join((node.pprint(depth=depth + 1) for node in self.children))
        return f"{tabs}<{self.__class__.__name__}: {self.value.__repr__()}>\n{children}"

    def end_node(self) -> bool:
        return all(node.childless() for node in self.children)

    def childless(self) -> bool:
        return not isinstance(self, FunctionNode) and self.children == []

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
            node = VariableNode(token)
            return parser(tokens, node)

        case Token("constant"):
            node = ConstantNode(token)
            return parser(tokens, node)

        case Token("function"):
            args = parse_function_args(tokens)
            args = filter(None, (parser(iter(arg)) for arg in args))
            node = FunctionNode(token, list(args))
            return parser(tokens, node)

        # handles parenthesis precedence
        case Token("symbol", "("):
            expr = parse_parenthesis_expr(chain([token], tokens))
            node = ParenthesesNode(token, [parser(iter(expr), parent)])
            return parser(tokens, node)

        # handles right associative unary operator (%)
        case Token("operator", "%") if parent is not None:
            node = FunctionNode(token, [parent])
            return parser(tokens, node)

        # handles left associative unary operators
        case Token("operator", "+" | "-") if parent is None:
            peek = next(tokens)
            token = Token("operator", f"unary {token.value}")
            # unary left operator only allowed when:
            # - operator plus and minus
            # - start of expression or parser called from the operator case
            # - next token is a variable, constant or parenthesis expression
            match peek:
                case Token("variable"):
                    node = FunctionNode(token, [VariableNode(peek)])
                case Token("constant"):
                    node = FunctionNode(token, [ConstantNode(peek)])
                case Token("symbol", "("):
                    tokens = chain([peek], tokens)  # re-insert left parenthesis
                    node = FunctionNode(token, [parser(tokens)])
                case _:
                    raise SyntaxError(f"Invalid unary expression for token: {token}")
            return parser(tokens, node)

        # handles binary operators
        case Token("operator") if parent is not None:
            left = parent
            right = parser(tokens)

            # receives parent = none when a operator case call parser(tokens) or when operator in the beginning of a expression
            # receives left_operand = none when expression ends in a operator
            if left is None or right is None:
                raise SyntaxError(f"Invalid right side operand: {token}")

            # hacky way to handle minus sign, transforms '2 - 1' into '2 + (-1)'
            # if right operand is a FunctionNode, applies unary - to the first children
            MINUS = Token("operator", "unary -")
            if token.value == "-" and isinstance(right, FunctionNode):
                sub_node = FunctionNode(MINUS, [right.children.pop(0)])
                right.children.insert(0, sub_node)
                token = Token("operator", "+")
            elif token.value == "-":
                right = FunctionNode(MINUS, [right])
                token = Token("operator", "+")

            # invert nodes if right priority > left priority
            if needs_swap(token, right.token):
                node = FunctionNode(token, [left, right.children.pop(0)])
                # need to check if token has priority over next children too
                # e.g. -> 1 ^ 2 * 3 + 4
                if needs_swap(token, node[1].token):
                    subnode = node.children.pop()
                    node.children.append(subnode.children.pop(0))
                    subnode.children.append(node)
                    node = subnode
                right.children.insert(0, node)
                return right

            return FunctionNode(token, [left, right])

        case _:
            raise SyntaxError(f"Invalid token: {token}")
