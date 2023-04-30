from operator import add, mod, mul, truediv
from parser import ASTNode, parser

from lexer import Token, lexer

OPERATIONS = {
    "+": add,
    "*": mul,
    "/": truediv,
    "%": mod,
    "//": lambda a, b: a - b,
    "IF": lambda a, b, c: b if a else c,
    "MIN": min,
    "MAX": max,
    "SUM": sum,
}


def interpreter(node, variables=None):
    if variables is None:
        variables = {}

    match (node.type, node.value, node.is_end_node):
        case ("constant", _, _):
            return node
        case ("boolean", _, _):
            node.value = node.value == "TRUE"
            return node
        case ("variable", _, _):
            print(node)
            value = variables[node.value]
            return ASTNode(Token("constant", value))
        case ("symbol", "(", _):
            return node.children[0]
        case (_, _, True):
            inputs = [c.value for c in node.children]
            fn = OPERATIONS[node.value]
            result = fn(*inputs)
            return ASTNode(Token("constant", result))
        case _:
            node.children = [
                interpreter(children, variables) for children in node.children
            ]
            return interpreter(node, variables)


if __name__ == "__main__":
    expr = "MAX(1, 2 + 3) + A12"
    vars = {"A12": 10}

    tokens = iter(lexer(expr))
    ast = parser(tokens)
    result = interpreter(ast, vars).value
    print(result)
