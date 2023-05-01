from parser import parser

from interpreter import interpreter
from lexer import lexer


def main(expr):
    tokens = lexer(expr)
    ast = parser(iter(tokens))
    ast = interpreter(ast)
    print(ast.value)


if __name__ == "__main__":
    test = "1 * (2 + 3)"
    main(test)
