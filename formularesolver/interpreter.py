import math
import operator
from operator import add, mod, mul, truediv, xor
from parser import (ASTNode, ConstantNode, FunctionNode, ParenthesesNode,
                    VariableNode, parser)

from lexer import Token, lexer


def range_operator(a, b):
    pass


OPERATIONS = {
    # logical functions
    "AND": all,
    "OR": any,
    "XOR": xor,
    "IF": lambda a, b, c: b if a else c,
    "NOT": lambda a: not a,
    # operators
    "+": operator.add,
    "-": operator.sub,
    "unary -": lambda a: -1 * a,
    "unary +": lambda a: +1 * a,
    "*": operator.mul,
    "/": operator.truediv,
    "^": operator.pow,
    "%": lambda a: a / 100,
    "&": lambda a, b: "".join((a, b)),
    ":": range_operator,
    # math functions
    "ABS": abs,
    "COS": math.cos,
    "SIN": math.sin,
    "TAN": math.tan,
    "EXP": math.exp,
    "LOG": math.log,
    "LOG10": math.log10,
    "PI": lambda: math.pi,
    "CEIL": math.ceil,
    "FLOOR": math.floor,
    "MAX": max,
    "MIN": min,
    "ROUND": round,
    "SUM": sum,
}


def interpreter(node: ASTNode, variables=None) -> ASTNode:
    if variables is None:
        variables = {}

    match node:
        case ConstantNode(value=value):
            return node
        case VariableNode(value=value):
            value = variables[value]
            return ConstantNode(Token("constant", value))
        case ParenthesesNode(children=children):
            return children[0]
        case FunctionNode(value=value, children=children) if node.end_node():
            fn = OPERATIONS[value]
            result = fn(*(c.value for c in children))
            return ConstantNode(Token("constant", result))
        case ASTNode(children=children):
            node.children = [interpreter(child, variables) for child in children]
            return interpreter(node, variables)


def formula_resolver(expr: str):
    tokens = lexer(expr)
    ast = parser(tokens)
    print(ast)
    result = interpreter(ast)
    return result.token.value


if __name__ == "__main__":
    pass
    # expr = "1 + COS(2 * PI(1))"
    # print(formula_resolver(expr))
