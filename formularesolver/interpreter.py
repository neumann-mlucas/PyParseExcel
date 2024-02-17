import math
import operator
from parser import (ASTNode, ConstantNode, FunctionNode, ParenthesesNode,
                    VariableNode, parser)
from typing import Callable

from lexer import Token, lexer
from utils import excel_range


def range_operator(a: str, b: str, variables: dict) -> list:
    return [variables.get(v) for v in excel_range(a, b)]


OPERATIONS: dict[str, Callable] = {
    # logical functions
    "AND": lambda *args: all(args),
    "OR": lambda *args: any(args),
    "XOR": operator.xor,
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
    # logical operators
    "=": operator.eq,
    "<>": operator.ne,
    "<=": operator.le,
    ">=": operator.ge,
    ">": operator.gt,
    "<": operator.lt,
}


def interpreter(node: ASTNode, variables: dict) -> ASTNode:
    match node:
        case ConstantNode(value=value):
            return node
        case VariableNode(value=value):
            var_value = variables[value]
            return ConstantNode(Token("constant", var_value))
        case ParenthesesNode(children=children):
            return children[0]
        case FunctionNode(value=value, children=children) if node.end_node():
            fn = OPERATIONS[value]
            if need_refs(value):
                result = fn(*(c.value for c in children), variables=variables)
            else:
                result = fn(*(c.value for c in children))
            return ConstantNode(Token("constant", result))
        case ASTNode(children=children):
            node.children = [interpreter(child, variables) for child in children]
            return interpreter(node, variables)


def need_refs(function: str) -> bool:
    return function in (":")


def formula_resolver(expr: str, variables: dict | None = None):
    if variables is None:
        variables = {}
    tokens = lexer(expr)
    ast = parser(tokens)
    # print(ast)
    result = interpreter(ast, variables)
    return result.value


if __name__ == "__main__":
    variables = {
        "A1": 1,
        "A2": 1,
        "A3": 1,
        "A4": 1,
        "A5": 1,
        "A6": 1,
        "A7": 1,
        "A8": 1,
        "A9": 1,
        "A10": 1,
    }
    expr = "SUM(A1:A10) + COS(2 * PI())"
    print(formula_resolver(expr, variables))
